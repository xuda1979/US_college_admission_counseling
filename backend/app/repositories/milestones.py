from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDRepository
from ..models.milestone import Milestone


class MilestoneRepository(CRUDRepository[Milestone]):
    async def list_for_applicant(self, db: AsyncSession, applicant_id: int) -> list[Milestone]:
        result = await db.execute(
            select(Milestone).where(Milestone.applicant_id == applicant_id).order_by(Milestone.due_date)
        )
        return result.scalars().all()


milestone_repository = MilestoneRepository(Milestone)
