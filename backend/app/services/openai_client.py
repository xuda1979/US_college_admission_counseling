import json
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


class MockOpenAIClient:
    def __init__(self) -> None:
        self.model = "mock-gpt"

    async def complete(self, messages: list[Mapping[str, Any]]) -> str:
        # Determine the context based on messages
        content = ""
        for message in messages:
            content += str(message.get("content", ""))

        if "Evaluate the following applicant" in content:
            return json.dumps({
                "scores": {
                    "academics": 8.5,
                    "extracurriculars": 7.0,
                    "essays": 6.0,
                    "overall_fit": 7.5
                },
                "summary": "The applicant shows strong academic potential but needs to improve extracurricular engagement.",
                "suggestions": [
                    {
                        "title": "Boost Extracurriculars",
                        "action": "Join a club or take on a leadership role.",
                        "impact": "High",
                        "effort": "Medium",
                        "deadline": "2023-12-01"
                    },
                    {
                        "title": "Refine Essay",
                        "action": "Focus on a specific anecdote that highlights personal growth.",
                        "impact": "High",
                        "effort": "High",
                        "deadline": "2023-11-15"
                    },
                     {
                        "title": "Prepare for Interviews",
                        "action": "Practice with mock interviews.",
                        "impact": "Medium",
                        "effort": "Medium",
                        "deadline": "2024-01-10"
                    }
                ]
            })
        elif "You are an admissions essay coach" in content:
            return json.dumps({
                "strengths": [
                    "Strong opening hook",
                    "Clear voice",
                    "Good use of imagery"
                ],
                "areas_for_improvement": [
                    "Conclusion is weak",
                    "Transition between paragraphs could be smoother"
                ],
                "revision_plan": [
                    "Rewrite the conclusion to summarize the main points",
                    "Add transition sentences between paragraphs 2 and 3"
                ]
            })
        else:
            return "Mock response from OpenAI."


async def get_openai_client() -> OpenAIClient | MockOpenAIClient:
    settings = get_settings()
    if settings.mock_openai:
        return MockOpenAIClient()
    return OpenAIClient()
