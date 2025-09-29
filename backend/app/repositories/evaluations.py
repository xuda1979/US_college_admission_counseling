from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDRepository
from ..models.evaluation import Evaluation


class EvaluationRepository(CRUDRepository[Evaluation]):
    async def list_for_applicant(self, db: AsyncSession, applicant_id: int) -> list[Evaluation]:
        result = await db.execute(
            select(Evaluation).where(Evaluation.applicant_id == applicant_id).order_by(Evaluation.created_at.desc())
        )
        return result.scalars().all()


evaluation_repository = EvaluationRepository(Evaluation)
