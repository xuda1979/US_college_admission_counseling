from datetime import datetime

from pydantic import BaseModel


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

    class Config:
        orm_mode = True
