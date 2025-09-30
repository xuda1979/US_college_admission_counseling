from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SuggestionRead(BaseModel):
    id: int
    evaluation_id: int
    title: str
    description: str
    impact: str | None = None
    effort: str | None = None
    deadline: datetime | None = None
    acknowledged_at: datetime | None = None
    is_archived: bool = False

    model_config = ConfigDict(from_attributes=True)
