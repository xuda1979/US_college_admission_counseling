from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from ..db.base_class import Base


class Suggestion(Base):
    __tablename__ = "suggestions"

    id = Column(Integer, primary_key=True, index=True)
    evaluation_id = Column(Integer, ForeignKey("evaluations.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    impact = Column(String, nullable=True)
    effort = Column(String, nullable=True)
    deadline = Column(DateTime, nullable=True)
    acknowledged_at = Column(DateTime, nullable=True)
    is_archived = Column(Boolean, default=False, nullable=False)

    evaluation = relationship("Evaluation", back_populates="suggestions")
