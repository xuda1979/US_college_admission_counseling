from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..api.deps import get_current_applicant
from ..db.session import get_db
from ..repositories.milestones import milestone_repository
from ..schemas.milestone import MilestoneRead

router = APIRouter(prefix="/milestones", tags=["milestones"])


@router.get("/", response_model=list[MilestoneRead])
async def list_milestones(current_user=Depends(get_current_applicant), db: AsyncSession = Depends(get_db)):
    return await milestone_repository.list_for_applicant(db, current_user.id)
