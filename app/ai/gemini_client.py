from typing import Any, Dict, List, Optional
import httpx
from app.ai.chat_client import BaseLLMClient
from app.core.config import settings
from app.core.logging import logger
from app.utils.exceptions import AIInferenceException


class GeminiClient(BaseLLMClient):
    """Google Gemini API client using standard HTTP requests."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model = "gemini-1.5-flash"
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    async def generate_response(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.2,
    ) -> str:
        if not self.api_key:
            raise AIInferenceException("Missing GEMINI_API_KEY in environment configuration.")

        url = f"{self.base_url}/{self.model}:generateContent?key={self.api_key}"
        
        full_text = prompt
        if system_instruction:
            full_text = f"System Instructions:\n{system_instruction}\n\nUser Request:\n{prompt}"

        payload = {
            "contents": [
                {
                    "parts": [{"text": full_text}]
                }
            ],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": 1000,
            }
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, json=payload)
                if response.status_code != 200:
                    logger.error(f"Gemini API error ({response.status_code}): {response.text}")
                    raise AIInferenceException(f"Gemini API error: HTTP {response.status_code}")
                
                data = response.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "").strip()
                return "I could not generate a response from the model."
        except Exception as e:
            logger.error(f"Gemini generation exception: {str(e)}")
            raise AIInferenceException(f"Gemini service unavailable: {str(e)}")

    async def generate_chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.2,
    ) -> str:
        prompt = "\n".join([f"{m.get('role', 'user')}: {m.get('content', '')}" for m in messages])
        return await self.generate_response(prompt=prompt, temperature=temperature)
