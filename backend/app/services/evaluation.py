from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from ..models.applicant import Applicant
from ..repositories.academic_records import academic_record_repository
from ..repositories.evaluations import evaluation_repository
from ..repositories.extracurriculars import extracurricular_repository
from ..repositories.suggestions import suggestion_repository
from .openai_client import OpenAIClient


@dataclass
class EvaluationResult:
    scores: dict[str, Any]
    summary: str
    suggestions: list[dict[str, Any]]


class EvaluationService:
    def __init__(self, openai_client: OpenAIClient):
        self.openai_client = openai_client

    async def evaluate_applicant(self, db: AsyncSession, applicant: Applicant) -> Any:
        academic_records = await academic_record_repository.list_for_applicant(db, applicant.id)
        extracurriculars = await extracurricular_repository.list_for_applicant(db, applicant.id)

        prompt_messages = self._build_prompt(applicant, academic_records, extracurriculars)
        content = await self.openai_client.complete(prompt_messages)
        result = self._parse_response(content)

        evaluation = await evaluation_repository.create(
            db,
            {
                "applicant_id": applicant.id,
                "model_name": self.openai_client.model,
                "scores": result.scores,
                "summary": result.summary,
                "recommendations": result.suggestions,
            },
        )

        for suggestion in result.suggestions:
            await suggestion_repository.create(
                db,
                {
                    "evaluation_id": evaluation.id,
                    "title": suggestion.get("title", "Recommendation"),
                    "description": suggestion.get("action", ""),
                    "impact": suggestion.get("impact"),
                    "effort": suggestion.get("effort"),
                    "deadline": suggestion.get("deadline"),
                },
            )

        return evaluation

    def _build_prompt(self, applicant: Applicant, academic_records, extracurriculars) -> list[dict[str, str]]:
        academics = "\n".join(
            f"School: {record.school_name}, GPA: {record.gpa}, Coursework: {record.coursework}" for record in academic_records
        )
        activities = "\n".join(
            f"{activity.name} - {activity.role} ({activity.impact})" for activity in extracurriculars
        )

        return [
            {
                "role": "system",
                "content": "You are a seasoned US university admissions counselor providing holistic feedback.",
            },
            {
                "role": "user",
                "content": (
                    "Evaluate the following applicant. Provide numeric scores (0-10) for academics, extracurricular impact, essays, and overall fit, "
                    "along with a narrative summary and 3 prioritized improvement suggestions. Return valid JSON with keys "
                    "'scores', 'summary', and 'suggestions'. Each suggestion needs 'title', 'action', 'impact', 'effort', and optional 'deadline'.\n"
                    f"Applicant: {applicant.full_name}\nTarget Schools: {applicant.target_schools or 'Not specified'}\n"
                    f"Academics:\n{academics or 'No academic record yet.'}\n"
                    f"Activities:\n{activities or 'No extracurriculars provided.'}"
                ),
            },
        ]

    def _parse_response(self, content: str) -> EvaluationResult:
        import json

        try:
            payload = json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Unable to parse evaluation response: {exc}") from exc

        return EvaluationResult(
            scores=payload.get("scores", {}),
            summary=payload.get("summary", ""),
            suggestions=payload.get("suggestions", []),
        )
