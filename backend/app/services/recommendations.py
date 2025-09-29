from collections.abc import Sequence
from datetime import datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from ..models.evaluation import Evaluation
from ..repositories.milestones import milestone_repository
from ..repositories.suggestions import suggestion_repository
from .openai_client import OpenAIClient


class RecommendationService:
    def __init__(self, openai_client: OpenAIClient):
        self.openai_client = openai_client

    async def refresh_recommendations(
        self, db: AsyncSession, evaluation: Evaluation, context: Sequence[dict[str, Any]] | None = None
    ) -> list[dict[str, Any]]:
        prompt = self._build_prompt(evaluation, context)
        response = await self.openai_client.complete(prompt)
        suggestions = self._parse_response(response)

        saved_suggestions = []
        for suggestion in suggestions:
            deadline = self._parse_datetime(suggestion.get("deadline"))
            record = await suggestion_repository.create(
                db,
                {
                    "evaluation_id": evaluation.id,
                    "title": suggestion.get("title", "Recommendation"),
                    "description": suggestion.get("action", ""),
                    "impact": suggestion.get("impact"),
                    "effort": suggestion.get("effort"),
                    "deadline": deadline,
                },
            )
            saved_suggestions.append(record)
            if deadline:
                await milestone_repository.create(
                    db,
                    {
                        "applicant_id": evaluation.applicant_id,
                        "title": record.title,
                        "description": record.description,
                        "due_date": deadline,
                    },
                )

        return suggestions

    def _build_prompt(self, evaluation: Evaluation, context: Sequence[dict[str, Any]] | None) -> list[dict[str, str]]:
        context_lines = "\n".join(f"- {item['area']}: {item['detail']}" for item in context or [])
        return [
            {
                "role": "system",
                "content": "You are creating actionable improvement plans for college applicants.",
            },
            {
                "role": "user",
                "content": (
                    "Draft three prioritized recommendations that will materially strengthen the applicant's profile. "
                    "Respond with JSON list under key 'suggestions', with fields: title, action, impact (High/Medium/Low), "
                    "effort (High/Medium/Low), and deadline (ISO format or null).\n"
                    f"Latest Evaluation Summary: {evaluation.summary}\n"
                    f"Existing Context:\n{context_lines or 'No additional context provided.'}"
                ),
            },
        ]

    def _parse_response(self, content: str) -> list[dict[str, Any]]:
        import json

        try:
            payload = json.loads(content)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Unable to parse recommendation response: {exc}") from exc
        return payload.get("suggestions", [])

    def _parse_datetime(self, value: Any) -> datetime | None:
        if not value:
            return None
        if isinstance(value, datetime):
            return value
        try:
            return datetime.fromisoformat(value)
        except (TypeError, ValueError):
            return None
