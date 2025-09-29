from datetime import datetime
from typing import Any

from pydantic import BaseModel


class EvaluationRead(BaseModel):
    id: int
    applicant_id: int
    model_name: str
    scores: dict[str, Any] | None = None
    summary: str | None = None
    recommendations: list[dict[str, Any]] | None = None
    created_at: datetime | None = None

    class Config:
        orm_mode = True


class EvaluationRequest(BaseModel):
    applicant_id: int
