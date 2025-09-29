from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from ..db.base_class import Base


class Applicant(Base):
    __tablename__ = "applicants"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    target_schools = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    academic_records = relationship("AcademicRecord", back_populates="applicant", cascade="all, delete-orphan")
    extracurriculars = relationship("Extracurricular", back_populates="applicant", cascade="all, delete-orphan")
    essays = relationship("Essay", back_populates="applicant", cascade="all, delete-orphan")
    evaluations = relationship("Evaluation", back_populates="applicant", cascade="all, delete-orphan")
    milestones = relationship("Milestone", back_populates="applicant", cascade="all, delete-orphan")
