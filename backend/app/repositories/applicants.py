from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDRepository
from ..models.applicant import Applicant


class ApplicantRepository(CRUDRepository[Applicant]):
    async def get_by_email(self, db: AsyncSession, email: str) -> Applicant | None:
        return await self.get_by_field(db, "email", email)


applicant_repository = ApplicantRepository(Applicant)
