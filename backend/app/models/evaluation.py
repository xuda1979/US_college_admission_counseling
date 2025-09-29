from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import relationship

from ..db.base_class import Base


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    applicant_id = Column(Integer, ForeignKey("applicants.id", ondelete="CASCADE"), nullable=False, index=True)
    essay_id = Column(Integer, ForeignKey("essays.id", ondelete="SET NULL"), nullable=True)
    model_name = Column(String, nullable=False)
    scores = Column(JSON, nullable=True)
    summary = Column(Text, nullable=True)
    recommendations = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    applicant = relationship("Applicant", back_populates="evaluations")
    essay = relationship("Essay", back_populates="critiques")
    suggestions = relationship("Suggestion", back_populates="evaluation", cascade="all, delete-orphan")
