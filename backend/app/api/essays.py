from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..api.deps import get_current_applicant
from ..db.session import get_db
from ..repositories.essays import essay_repository
from ..schemas.essay import EssayCreate, EssayRead
from ..services.essays import EssayService
from ..services.openai_client import get_openai_client

router = APIRouter(prefix="/essays", tags=["essays"])


@router.post("/", response_model=EssayRead)
async def create_essay(essay_in: EssayCreate, current_user=Depends(get_current_applicant), db: AsyncSession = Depends(get_db)):
    if essay_in.applicant_id != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot create essays for other applicants")
    essay = await essay_repository.create(db, essay_in.dict())
    return essay


@router.post("/{essay_id}/critique")
async def request_critique(
    essay_id: int,
    current_user=Depends(get_current_applicant),
    db: AsyncSession = Depends(get_db),
):
    essay = await essay_repository.get(db, essay_id)
    if not essay or essay.applicant_id != current_user.id:
        raise HTTPException(status_code=404, detail="Essay not found")

    client = await get_openai_client()
    service = EssayService(client)
    evaluation = await service.critique(db, essay)
    return {"evaluation_id": evaluation.id, "summary": evaluation.summary}


@router.get("/", response_model=list[EssayRead])
async def list_essays(current_user=Depends(get_current_applicant), db: AsyncSession = Depends(get_db)):
    return await essay_repository.list_for_applicant(db, current_user.id)
