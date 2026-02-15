from fastapi import APIRouter, HTTPException

from app.models.schemas import AnalysisRequest, JobResult
from app.workers.job_manager import job_manager

router = APIRouter()


@router.post("/analyze")
async def analyze_entities(request: AnalysisRequest):
    try:
        job_id = job_manager.enqueue(request.entities)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"jobId": job_id, "message": "Analysis queued"}


@router.get("/status/{job_id}")
async def get_status(job_id: str):
    status = job_manager.get_status(job_id)
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    return status


@router.get("/results/{job_id}", response_model=JobResult)
async def get_results(job_id: str):
    job = job_manager.get_results(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    status = job_manager.get_status(job_id)
    return JobResult(job_id=job_id, status=status, rankings=job.results)
