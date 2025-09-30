from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EssayCreate(BaseModel):
    applicant_id: int
    prompt: str
    content: str


class EssayRead(BaseModel):
    id: int
    applicant_id: int
    prompt: str
    content: str
    version: int | None = None
    created_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
