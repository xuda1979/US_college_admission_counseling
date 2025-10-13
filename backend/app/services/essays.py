import json
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from ..models.essay import Essay
from ..repositories.evaluations import evaluation_repository
from .openai_client import OpenAIClient


essay_feedback_prompt = """
You are an admissions essay coach. Provide concise feedback on structure, storytelling, voice, and alignment with the prompt.
Return JSON with keys 'strengths', 'areas_for_improvement', and 'revision_plan'.
"""


class EssayService:
    def __init__(self, openai_client: OpenAIClient):
        self.openai_client = openai_client

    async def critique(self, db: AsyncSession, essay: Essay) -> Any:
        messages = [
            {"role": "system", "content": essay_feedback_prompt.strip()},
            {
                "role": "user",
                "content": f"Prompt: {essay.prompt}\nEssay Draft:\n{essay.content}",
            },
        ]
        content = await self.openai_client.complete(messages)
        summary = self._summarize_feedback(content)
        evaluation = await evaluation_repository.create(
            db,
            {
                "applicant_id": essay.applicant_id,
                "essay_id": essay.id,
                "model_name": self.openai_client.model,
                "summary": summary,
            },
        )
        return evaluation

    def _summarize_feedback(self, content: str) -> str:
        try:
            payload = json.loads(content)
        except json.JSONDecodeError:
            return content.strip()

        sections: list[str] = []
        mapping = {
            "Strengths": payload.get("strengths"),
            "Areas for improvement": payload.get("areas_for_improvement"),
            "Revision plan": payload.get("revision_plan"),
        }

        for title, value in mapping.items():
            formatted = self._format_section(title, value)
            if formatted:
                sections.append(formatted)

        if sections:
            return "\n\n".join(sections)
        return content.strip()

    def _format_section(self, title: str, value: Any) -> str | None:
        if value is None:
            return None
        if isinstance(value, str):
            text = value.strip()
            return f"{title}: {text}" if text else None
        if isinstance(value, list):
            items = [str(item).strip() for item in value if str(item).strip()]
            if not items:
                return None
            bullet_list = "\n".join(f"- {item}" for item in items)
            return f"{title}:\n{bullet_list}"
        if isinstance(value, dict):
            items = [f"{key}: {str(val).strip()}" for key, val in value.items() if str(val).strip()]
            if not items:
                return None
            bullet_list = "\n".join(f"- {item}" for item in items)
            return f"{title}:\n{bullet_list}"
        text = str(value).strip()
        return f"{title}: {text}" if text else None
