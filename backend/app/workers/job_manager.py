from __future__ import annotations

import asyncio
import uuid
from datetime import datetime

from app.core.config import settings
from app.models.job_store import JobRecord
from app.models.schemas import JobState, JobStatus
from app.services.analysis_service import analysis_service


class JobManager:
    def __init__(self) -> None:
        self._jobs: dict[str, JobRecord] = {}

    def enqueue(self, entities: list[str]) -> str:
        if len(entities) > settings.max_entities_per_job:
            raise ValueError(f"Maximum entities per job is {settings.max_entities_per_job}")

        job_id = str(uuid.uuid4())
        self._jobs[job_id] = JobRecord(job_id=job_id, entities=entities)
        asyncio.create_task(self._run_job(job_id))
        return job_id

    async def _run_job(self, job_id: str) -> None:
        job = self._jobs[job_id]
        job.state = JobState.running
        job.updated_at = datetime.utcnow()

        try:
            total = len(job.entities)
            for idx, identifier in enumerate(job.entities, start=1):
                analyzed = await analysis_service.analyze_entity(identifier)
                from app.models.schemas import FeasibilityAnalysis

                job.results.append(FeasibilityAnalysis(**analyzed))
                job.progress = idx / total
                job.updated_at = datetime.utcnow()

            job.results = sorted(job.results, key=lambda r: r.confidence_score, reverse=True)
            job.state = JobState.completed
            job.updated_at = datetime.utcnow()
        except Exception as exc:
            job.state = JobState.failed
            job.error = str(exc)
            job.updated_at = datetime.utcnow()

    def get_status(self, job_id: str) -> JobStatus | None:
        job = self._jobs.get(job_id)
        if not job:
            return None
        return JobStatus(
            job_id=job.job_id,
            state=job.state,
            progress=job.progress,
            submitted_at=job.submitted_at,
            updated_at=job.updated_at,
            error=job.error,
        )

    def get_results(self, job_id: str):
        return self._jobs.get(job_id)


job_manager = JobManager()
