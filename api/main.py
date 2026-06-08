"""
FastAPI Backend - REST API for the Multi-Agent Research System.
Allows programmatic access and future mobile/web app integration.
"""
import uuid
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict
import asyncio

from src.config.settings import settings
from src.utils.logger import app_logger

from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Multi-Agent Research API",
    description="API for the Multi-Agent Research & Report Generation System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

import os
# Create static directory if it doesn't exist
os.makedirs("static", exist_ok=True)
app.mount("/dashboard", StaticFiles(directory="static", html=True), name="static")


# CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory job store (use Redis for production)
job_store: Dict[str, dict] = {}


class ResearchRequest(BaseModel):
    topic: str
    instructions: Optional[str] = None
    max_iterations: int = 10


class ResearchResponse(BaseModel):
    job_id: str
    status: str
    message: str


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Multi-Agent Research System",
        "version": "1.0.0",
    }


@app.post("/api/research", response_model=ResearchResponse)
async def start_research(
    request: ResearchRequest,
    background_tasks: BackgroundTasks,
):
    """Start an asynchronous research job."""
    job_id = str(uuid.uuid4())
    job_store[job_id] = {
        "status": "pending",
        "topic": request.topic,
        "result": None,
        "error": None,
    }

    background_tasks.add_task(
        _run_research_background,
        job_id,
        request.topic,
        request.instructions,
        request.max_iterations,
    )

    return ResearchResponse(
        job_id=job_id,
        status="pending",
        message=f"Research started for: {request.topic}",
    )


@app.get("/api/research/{job_id}")
async def get_research_status(job_id: str):
    """Get the status and result of a research job."""
    if job_id not in job_store:
        raise HTTPException(status_code=404, detail="Job not found")
    return job_store[job_id]


async def _run_research_background(
    job_id: str,
    topic: str,
    instructions: Optional[str],
    max_iterations: int,
):
    """Background task to run the research pipeline."""
    from src.graph.workflow import run_research_pipeline

    job_store[job_id]["status"] = "running"
    app_logger.info(f"Background research job {job_id} started")

    try:
        result = run_research_pipeline(
            topic=topic,
            user_instructions=instructions,
            max_iterations=max_iterations,
        )

        job_store[job_id].update({
            "status": "complete",
            "result": {
                "final_report": result.final_report,
                "sources": result.sources,
                "quality_score": result.critic_feedback.score if result.critic_feedback else None,
                "credibility": result.fact_check_result.overall_credibility if result.fact_check_result else None,
            }
        })

    except Exception as e:
        app_logger.error(f"Job {job_id} failed: {e}")
        job_store[job_id].update({
            "status": "failed",
            "error": str(e),
        })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True,
    )