from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..api.deps import get_current_applicant
from ..db.session import get_db
from ..repositories.evaluations import evaluation_repository
from ..schemas.evaluation import EvaluationRead
from ..services.evaluation import EvaluationService
from ..services.openai_client import get_openai_client

router = APIRouter(prefix="/evaluations", tags=["evaluations"])


@router.post("/trigger", response_model=EvaluationRead)
async def trigger_evaluation(
    current_user=Depends(get_current_applicant),
    db: AsyncSession = Depends(get_db),
):
    client = await get_openai_client()
    service = EvaluationService(client)
    evaluation = await service.evaluate_applicant(db, current_user)
    return evaluation


@router.get("/", response_model=list[EvaluationRead])
async def list_evaluations(
    current_user=Depends(get_current_applicant), db: AsyncSession = Depends(get_db)
):
    return await evaluation_repository.list_for_applicant(db, current_user.id)


@router.get("/{evaluation_id}", response_model=EvaluationRead)
async def get_evaluation(
    evaluation_id: int,
    current_user=Depends(get_current_applicant),
    db: AsyncSession = Depends(get_db),
):
    evaluation = await evaluation_repository.get(db, evaluation_id)
    if not evaluation or evaluation.applicant_id != current_user.id:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    return evaluation
