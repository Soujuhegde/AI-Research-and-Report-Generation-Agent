"""
API Rate Limiting Middleware.
Prevents abuse of the research endpoints.
Uses slowapi (Starlette-compatible limiter).
"""
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, Response
from fastapi.responses import JSONResponse
import time
from collections import defaultdict
from src.utils.logger import app_logger


# Create limiter instance
limiter = Limiter(key_func=get_remote_address)


def get_limiter() -> Limiter:
    """Return the configured rate limiter."""
    return limiter


class RequestLoggingMiddleware:
    """
    ASGI Middleware that logs all incoming requests.
    Tracks response time and status codes.
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            start_time = time.time()
            request = Request(scope, receive)

            # Log request
            app_logger.info(
                f"→ {request.method} {request.url.path} "
                f"from {request.client.host if request.client else 'unknown'}"
            )

            # Track response
            status_code = [200]

            async def send_wrapper(message):
                if message["type"] == "http.response.start":
                    status_code[0] = message["status"]
                await send(message)

            await self.app(scope, receive, send_wrapper)

            duration = (time.time() - start_time) * 1000
            app_logger.info(
                f"← {status_code[0]} {request.url.path} "
                f"[{duration:.1f}ms]"
            )
        else:
            await self.app(scope, receive, send)


class BudgetGuardMiddleware:
    """
    Middleware that tracks API usage per IP.
    Enforces cost budget caps per session.
    """

    def __init__(self, app, max_requests_per_hour: int = 10):
        self.app = app
        self.max_requests = max_requests_per_hour
        self.request_counts = defaultdict(list)

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            client_ip = request.client.host if request.client else "unknown"

            # Only guard research endpoints
            if "/api/research" in request.url.path and request.method == "POST":
                now = time.time()
                hour_ago = now - 3600

                # Clean old requests
                self.request_counts[client_ip] = [
                    t for t in self.request_counts[client_ip] if t > hour_ago
                ]

                if len(self.request_counts[client_ip]) >= self.max_requests:
                    app_logger.warning(
                        f"Budget guard triggered for IP: {client_ip}"
                    )
                    response = JSONResponse(
                        status_code=429,
                        content={
                            "error": "Rate limit exceeded",
                            "message": (
                                f"Maximum {self.max_requests} research requests "
                                f"per hour allowed. Please wait before retrying."
                            ),
                            "retry_after_seconds": 3600,
                        }
                    )
                    await response(scope, receive, send)
                    return

                self.request_counts[client_ip].append(now)

        await self.app(scope, receive, send)