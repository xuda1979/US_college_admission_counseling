from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDRepository
from ..models.academic_record import AcademicRecord


class AcademicRecordRepository(CRUDRepository[AcademicRecord]):
    async def list_for_applicant(self, db: AsyncSession, applicant_id: int) -> list[AcademicRecord]:
        result = await db.execute(select(AcademicRecord).where(AcademicRecord.applicant_id == applicant_id))
        return result.scalars().all()


academic_record_repository = AcademicRecordRepository(AcademicRecord)
