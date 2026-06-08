"""
Research Routes - Endpoints for managing research jobs.
Full async implementation with background task processing.
"""
import uuid
import json
import os
from datetime import datetime
from typing import Optional, List

from fastapi import APIRouter, HTTPException, BackgroundTasks, Query
from pydantic import BaseModel, Field

from src.config.settings import settings
from src.utils.logger import app_logger

router = APIRouter(prefix="/api/research", tags=["research"])

# In-memory job store
# For production: replace with Redis or a database
job_store: dict = {}


# ─── Request / Response Models ────────────────────────────────────────────────

class ResearchRequest(BaseModel):
    topic: str = Field(..., min_length=3, max_length=500, description="Research topic")
    instructions: Optional[str] = Field(
        None, max_length=1000, description="Additional instructions for agents"
    )
    max_iterations: int = Field(default=10, ge=3, le=20)
    max_revisions: int = Field(default=2, ge=0, le=3)


class JobStatus(BaseModel):
    job_id: str
    status: str  # pending | running | complete | failed
    topic: str
    created_at: str
    completed_at: Optional[str] = None
    progress_percent: int = 0
    current_agent: Optional[str] = None
    result: Optional[dict] = None
    error: Optional[str] = None


class ResearchListItem(BaseModel):
    job_id: str
    topic: str
    status: str
    created_at: str


# ─── Routes ───────────────────────────────────────────────────────────────────

@router.post("/", response_model=JobStatus, status_code=202)
async def start_research(
    request: ResearchRequest,
    background_tasks: BackgroundTasks,
):
    """
    Start a new asynchronous research job.
    Returns job_id immediately; poll GET /api/research/{job_id} for status.
    """
    job_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()

    job_store[job_id] = {
        "job_id": job_id,
        "status": "pending",
        "topic": request.topic,
        "created_at": created_at,
        "completed_at": None,
        "progress_percent": 0,
        "current_agent": None,
        "result": None,
        "error": None,
    }

    background_tasks.add_task(
        _run_research_background,
        job_id=job_id,
        topic=request.topic,
        instructions=request.instructions,
        max_iterations=request.max_iterations,
    )

    app_logger.info(f"Research job {job_id} queued for topic: '{request.topic}'")
    return job_store[job_id]


@router.get("/{job_id}", response_model=JobStatus)
async def get_research_status(job_id: str):
    """Get the current status and result of a research job."""
    if job_id not in job_store:
        raise HTTPException(
            status_code=404,
            detail=f"Job '{job_id}' not found. It may have expired."
        )
    return job_store[job_id]


@router.get("/", response_model=List[ResearchListItem])
async def list_research_jobs(
    limit: int = Query(default=20, ge=1, le=100),
    status: Optional[str] = Query(default=None),
):
    """List all research jobs, optionally filtered by status."""
    jobs = list(job_store.values())

    if status:
        jobs = [j for j in jobs if j["status"] == status]

    # Sort by created_at descending
    jobs.sort(key=lambda x: x["created_at"], reverse=True)
    return jobs[:limit]


@router.delete("/{job_id}")
async def delete_research_job(job_id: str):
    """Delete a research job from the store."""
    if job_id not in job_store:
        raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found")

    del job_store[job_id]
    return {"message": f"Job {job_id} deleted successfully"}


@router.get("/{job_id}/report")
async def get_report_only(job_id: str):
    """Get only the final report text for a completed job."""
    if job_id not in job_store:
        raise HTTPException(status_code=404, detail="Job not found")

    job = job_store[job_id]

    if job["status"] != "complete":
        raise HTTPException(
            status_code=400,
            detail=f"Job is not complete yet. Current status: {job['status']}"
        )

    return {
        "job_id": job_id,
        "topic": job["topic"],
        "report": job["result"]["final_report"] if job["result"] else None,
        "sources": job["result"]["sources"] if job["result"] else [],
    }


# ─── Background Worker ────────────────────────────────────────────────────────

async def _run_research_background(
    job_id: str,
    topic: str,
    instructions: Optional[str],
    max_iterations: int,
):
    """
    Background task: runs the full multi-agent research pipeline.
    Updates job_store at each stage.
    """
    from src.graph.workflow import run_research_pipeline

    app_logger.info(f"🚀 Background job {job_id} starting...")

    # Update to running
    job_store[job_id].update({
        "status": "running",
        "progress_percent": 10,
        "current_agent": "planner",
    })

    try:
        # Run pipeline (synchronous call in async context)
        import asyncio
        loop = asyncio.get_event_loop()
        final_state = await loop.run_in_executor(
            None,
            lambda: run_research_pipeline(
                topic=topic,
                user_instructions=instructions,
                max_iterations=max_iterations,
                thread_id=job_id,
            )
        )

        # Save report to disk
        _save_report_to_disk(job_id, topic, final_state)

        # Update job as complete
        job_store[job_id].update({
            "status": "complete",
            "progress_percent": 100,
            "current_agent": "complete",
            "completed_at": datetime.utcnow().isoformat(),
            "result": {
                "final_report": final_state.final_report,
                "draft_report": final_state.draft_report,
                "sources": final_state.sources,
                "quality_score": (
                    final_state.critic_feedback.score
                    if final_state.critic_feedback else None
                ),
                "credibility": (
                    final_state.fact_check_result.overall_credibility
                    if final_state.fact_check_result else None
                ),
                "revision_count": final_state.revision_count,
                "total_sources": len(final_state.sources),
            }
        })

        app_logger.info(f"✅ Job {job_id} completed successfully")

    except Exception as e:
        app_logger.error(f"❌ Job {job_id} failed: {e}")
        job_store[job_id].update({
            "status": "failed",
            "completed_at": datetime.utcnow().isoformat(),
            "error": str(e),
            "progress_percent": 0,
        })


def _save_report_to_disk(job_id: str, topic: str, final_state):
    """Persist the completed report to disk as JSON."""
    try:
        report_data = {
            "job_id": job_id,
            "topic": topic,
            "report": final_state.final_report,
            "sources": final_state.sources,
            "created_at": datetime.utcnow().isoformat(),
            "metadata": {
                "quality_score": (
                    final_state.critic_feedback.score
                    if final_state.critic_feedback else None
                ),
                "credibility": (
                    final_state.fact_check_result.overall_credibility
                    if final_state.fact_check_result else None
                ),
            }
        }

        filename = f"{job_id}_{topic[:30].replace(' ', '_')}.json"
        filepath = os.path.join(settings.reports_dir, filename)

        os.makedirs(settings.reports_dir, exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)

        app_logger.info(f"💾 Report saved to: {filepath}")

    except Exception as e:
        app_logger.warning(f"Could not save report to disk: {e}")