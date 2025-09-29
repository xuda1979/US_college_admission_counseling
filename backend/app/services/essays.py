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
        evaluation = await evaluation_repository.create(
            db,
            {
                "applicant_id": essay.applicant_id,
                "essay_id": essay.id,
                "model_name": self.openai_client.model,
                "summary": content,
            },
        )
        return evaluation
