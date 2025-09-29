from collections.abc import Mapping
from typing import Any

from openai import AsyncOpenAI

from ..core.config import get_settings


class OpenAIClient:
    def __init__(self) -> None:
        settings = get_settings()
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is not configured")
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model

    async def complete(self, messages: list[Mapping[str, Any]]) -> str:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.3,
        )
        choice = response.choices[0]
        return choice.message.content or ""


async def get_openai_client() -> OpenAIClient:
    return OpenAIClient()
