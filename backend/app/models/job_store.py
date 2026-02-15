from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from app.models.schemas import FeasibilityAnalysis, JobState


@dataclass
class JobRecord:
    job_id: str
    entities: list[str]
    state: JobState = JobState.queued
    progress: float = 0.0
    submitted_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    results: list[FeasibilityAnalysis] = field(default_factory=list)
    error: str | None = None
