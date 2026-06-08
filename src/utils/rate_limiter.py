import time
import threading
from collections import deque
from src.utils.logger import app_logger


class RateLimiter:
    """
    Token bucket rate limiter to prevent API cost explosion.
    Guards against runaway agent loops.
    """

    def __init__(self, max_calls: int = 10, period: float = 60.0):
        self.max_calls = max_calls
        self.period = period
        self.calls = deque()
        self.lock = threading.Lock()

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            self.wait()
            return func(*args, **kwargs)
        return wrapper

    def wait(self):
        with self.lock:
            now = time.time()
            # Remove old calls outside the window
            while self.calls and self.calls[0] < now - self.period:
                self.calls.popleft()

            if len(self.calls) >= self.max_calls:
                sleep_time = self.period - (now - self.calls[0])
                if sleep_time > 0:
                    app_logger.warning(
                        f"Rate limit reached. Sleeping {sleep_time:.2f}s"
                    )
                    time.sleep(sleep_time)

            self.calls.append(time.time())


class IterationGuard:
    """Prevents infinite agent loops."""

    def __init__(self, max_iterations: int = 10):
        self.max_iterations = max_iterations
        self.current = 0

    def check(self) -> bool:
        self.current += 1
        if self.current > self.max_iterations:
            app_logger.error(
                f"Max iterations ({self.max_iterations}) exceeded! Stopping agent."
            )
            return False
        return True

    def reset(self):
        self.current = 0