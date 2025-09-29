from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDRepository
from ..models.extracurricular import Extracurricular


class ExtracurricularRepository(CRUDRepository[Extracurricular]):
    async def list_for_applicant(self, db: AsyncSession, applicant_id: int) -> list[Extracurricular]:
        result = await db.execute(select(Extracurricular).where(Extracurricular.applicant_id == applicant_id))
        return result.scalars().all()


extracurricular_repository = ExtracurricularRepository(Extracurricular)
