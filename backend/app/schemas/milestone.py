from datetime import datetime

from pydantic import BaseModel


class MilestoneRead(BaseModel):
    id: int
    applicant_id: int
    title: str
    description: str | None = None
    due_date: datetime | None = None
    completed_at: datetime | None = None

    class Config:
        orm_mode = True
