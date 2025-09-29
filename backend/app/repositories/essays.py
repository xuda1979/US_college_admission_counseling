from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDRepository
from ..models.essay import Essay


class EssayRepository(CRUDRepository[Essay]):
    async def list_for_applicant(self, db: AsyncSession, applicant_id: int) -> list[Essay]:
        result = await db.execute(select(Essay).where(Essay.applicant_id == applicant_id).order_by(Essay.created_at.desc()))
        return result.scalars().all()


essay_repository = EssayRepository(Essay)
