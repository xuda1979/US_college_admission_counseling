from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..api.deps import get_current_applicant
from ..db.session import get_db
from ..repositories.evaluations import evaluation_repository
from ..repositories.suggestions import suggestion_repository
from ..schemas.suggestion import SuggestionRead
from ..services.openai_client import get_openai_client
from ..services.recommendations import RecommendationService

router = APIRouter(prefix="/suggestions", tags=["suggestions"])


@router.get("/", response_model=list[SuggestionRead])
async def list_suggestions(current_user=Depends(get_current_applicant), db: AsyncSession = Depends(get_db)):
    return await suggestion_repository.list_for_applicant(db, current_user.id)


@router.post("/refresh/{evaluation_id}", response_model=list[SuggestionRead])
async def refresh_suggestions(
    evaluation_id: int,
    current_user=Depends(get_current_applicant),
    db: AsyncSession = Depends(get_db),
):
    evaluation = await evaluation_repository.get(db, evaluation_id)
    if not evaluation or evaluation.applicant_id != current_user.id:
        raise HTTPException(status_code=404, detail="Evaluation not found")

    client = await get_openai_client()
    service = RecommendationService(client)
    await service.refresh_recommendations(db, evaluation)
    return await suggestion_repository.list_for_applicant(db, current_user.id)


@router.post("/{suggestion_id}/acknowledge", response_model=SuggestionRead)
async def acknowledge_suggestion(
    suggestion_id: int,
    current_user=Depends(get_current_applicant),
    db: AsyncSession = Depends(get_db),
):
    suggestion = await suggestion_repository.get(db, suggestion_id)
    if not suggestion:
        raise HTTPException(status_code=404, detail="Suggestion not found")

    evaluation = await evaluation_repository.get(db, suggestion.evaluation_id)
    if not evaluation or evaluation.applicant_id != current_user.id:
        raise HTTPException(status_code=404, detail="Suggestion not found")

    updated = await suggestion_repository.update(db, suggestion, {"acknowledged_at": datetime.utcnow()})
    return updated


@router.post("/{suggestion_id}/archive", response_model=SuggestionRead)
async def archive_suggestion(
    suggestion_id: int,
    current_user=Depends(get_current_applicant),
    db: AsyncSession = Depends(get_db),
):
    suggestion = await suggestion_repository.get(db, suggestion_id)
    if not suggestion:
        raise HTTPException(status_code=404, detail="Suggestion not found")

    evaluation = await evaluation_repository.get(db, suggestion.evaluation_id)
    if not evaluation or evaluation.applicant_id != current_user.id:
        raise HTTPException(status_code=404, detail="Suggestion not found")

    archived = await suggestion_repository.archive(db, suggestion)
    return archived
