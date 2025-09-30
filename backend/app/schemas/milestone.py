from datetime import datetime

from pydantic import BaseModel, ConfigDict


class MilestoneRead(BaseModel):
    id: int
    applicant_id: int
    title: str
    description: str | None = None
    due_date: datetime | None = None
    completed_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
