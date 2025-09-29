from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..db.base_class import Base


class Extracurricular(Base):
    __tablename__ = "extracurriculars"

    id = Column(Integer, primary_key=True, index=True)
    applicant_id = Column(Integer, ForeignKey("applicants.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=True)
    impact = Column(String, nullable=True)
    duration = Column(String, nullable=True)

    applicant = relationship("Applicant", back_populates="extracurriculars")
