from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class JobState(str, Enum):
    queued = "queued"
    running = "running"
    completed = "completed"
    failed = "failed"


class AnalysisRequest(BaseModel):
    entities: list[str] = Field(..., min_length=1, description="SMILES, InChI, ChEMBL IDs, CAS, etc.")


class ADMETRisk(BaseModel):
    logp: float | None = None
    solubility_class: str
    metabolic_liability: str
    tox_alerts: list[str] = Field(default_factory=list)
    overall_risk: str


class DrugLikeness(BaseModel):
    molecular_weight: float | None = None
    lipinski_violations: int
    lipe: float | None = None
    verdict: str


class FeasibilityAnalysis(BaseModel):
    input_identifier: str
    resolved_structure: str | None = None
    target_relevance: str
    mechanism_of_action: str
    predicted_activity: dict[str, Any]
    adme_tox: ADMETRisk
    synthetic_feasibility_score: float = Field(..., ge=0, le=1)
    drug_likeness: DrugLikeness
    pathway_or_disease_association: list[str] = Field(default_factory=list)
    confidence_score: float = Field(..., ge=0, le=1)
    recommendation: str
    rejection_or_promotion_reasons: list[str]


class JobStatus(BaseModel):
    job_id: str
    state: JobState
    progress: float = Field(..., ge=0, le=1)
    submitted_at: datetime
    updated_at: datetime
    error: str | None = None


class JobResult(BaseModel):
    job_id: str
    status: JobStatus
    rankings: list[FeasibilityAnalysis]
