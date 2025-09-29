from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDRepository
from ..models.evaluation import Evaluation
from ..models.suggestion import Suggestion


class SuggestionRepository(CRUDRepository[Suggestion]):
    async def list_for_applicant(self, db: AsyncSession, applicant_id: int) -> list[Suggestion]:
        result = await db.execute(
            select(Suggestion)
            .join(Evaluation)
            .where(Evaluation.applicant_id == applicant_id, Suggestion.is_archived.is_(False))
            .order_by(Suggestion.deadline)
        )
        return result.scalars().all()

    async def archive(self, db: AsyncSession, suggestion: Suggestion) -> Suggestion:
        return await self.update(db, suggestion, {"is_archived": True})


suggestion_repository = SuggestionRepository(Suggestion)
