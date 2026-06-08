"""
Health Check Routes - System status and diagnostics.
"""
import os
import sys
import time
from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any

from src.config.settings import settings
from src.utils.logger import app_logger

router = APIRouter(tags=["health"])

# Track app start time
START_TIME = time.time()


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    timestamp: str
    uptime_seconds: float
    environment: str


class DetailedHealthResponse(HealthResponse):
    checks: Dict[str, Any]
    python_version: str
    config: Dict[str, Any]


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Basic health check - returns immediately."""
    return HealthResponse(
        status="healthy",
        service="Multi-Agent Research System",
        version="1.0.0",
        timestamp=datetime.utcnow().isoformat(),
        uptime_seconds=round(time.time() - START_TIME, 2),
        environment=settings.app_env,
    )


@router.get("/health/detailed", response_model=DetailedHealthResponse)
async def detailed_health_check():
    """
    Detailed health check - verifies all external dependencies.
    Use for monitoring dashboards.
    """
    checks = {}

    # Check Tavily API connectivity
    try:
        from tavily import TavilyClient
        client = TavilyClient(api_key=settings.tavily_api_key)
        checks["tavily_api"] = {"status": "connected", "error": None}
    except Exception as e:
        checks["tavily_api"] = {"status": "error", "error": str(e)}

    # Check Sarvam API key is set
    checks["sarvam_api"] = {
        "status": "configured" if settings.sarvam_api_key else "missing",
        "model": settings.sarvam_model,
    }

    # Check disk space for reports directory
    try:
        os.makedirs(settings.reports_dir, exist_ok=True)
        stat = os.statvfs(settings.reports_dir)
        free_gb = (stat.f_frsize * stat.f_bavail) / (1024 ** 3)
        checks["disk_space"] = {
            "status": "ok" if free_gb > 0.5 else "low",
            "free_gb": round(free_gb, 2),
        }
    except Exception as e:
        checks["disk_space"] = {"status": "error", "error": str(e)}

    # Check LangGraph import
    try:
        import langgraph
        checks["langgraph"] = {"status": "ok", "version": langgraph.__version__}
    except Exception as e:
        checks["langgraph"] = {"status": "error", "error": str(e)}

    overall_status = (
        "healthy"
        if all(c.get("status") in ("ok", "connected", "configured")
               for c in checks.values())
        else "degraded"
    )

    return DetailedHealthResponse(
        status=overall_status,
        service="Multi-Agent Research System",
        version="1.0.0",
        timestamp=datetime.utcnow().isoformat(),
        uptime_seconds=round(time.time() - START_TIME, 2),
        environment=settings.app_env,
        checks=checks,
        python_version=sys.version,
        config={
            "max_iterations": settings.max_iterations,
            "max_search_results": settings.max_search_results,
            "sarvam_model": settings.sarvam_model,
            "reports_dir": settings.reports_dir,
        }
    )