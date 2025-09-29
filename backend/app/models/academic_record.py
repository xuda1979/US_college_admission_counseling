from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..db.base_class import Base


class AcademicRecord(Base):
    __tablename__ = "academic_records"

    id = Column(Integer, primary_key=True, index=True)
    applicant_id = Column(Integer, ForeignKey("applicants.id", ondelete="CASCADE"), nullable=False, index=True)
    school_name = Column(String, nullable=False)
    gpa = Column(Float, nullable=True)
    test_scores = Column(String, nullable=True)
    coursework = Column(String, nullable=True)

    applicant = relationship("Applicant", back_populates="academic_records")
