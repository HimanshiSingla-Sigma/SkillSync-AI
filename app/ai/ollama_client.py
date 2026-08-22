from typing import Any, Dict, List, Optional
import httpx
from app.ai.chat_client import BaseLLMClient
from app.core.config import settings
from app.core.logging import logger
from app.utils.exceptions import AIInferenceException


class OllamaClient(BaseLLMClient):
    """Local LLM client integrating with Ollama HTTP API."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        model_name: Optional[str] = None,
        timeout: Optional[float] = None,
    ):
        self.base_url = (base_url or settings.OLLAMA_BASE_URL).rstrip("/")
        self.model_name = model_name or settings.OLLAMA_MODEL
        self.timeout = timeout or settings.OLLAMA_REQUEST_TIMEOUT

    async def generate_response(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.2,
    ) -> str:
        url = f"{self.base_url}/api/generate"
        payload: Dict[str, Any] = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
            },
        }
        if system_instruction:
            payload["system"] = system_instruction

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload)
                if response.status_code != 200:
                    logger.error(
                        f"Ollama generation failed ({response.status_code}): {response.text}"
                    )
                    raise AIInferenceException(
                        f"Ollama error: status code {response.status_code}"
                    )

                data = response.json()
                return data.get("response", "").strip()
        except httpx.RequestError as e:
            logger.error(f"Network error communicating with Ollama service: {str(e)}")
            raise AIInferenceException(f"Failed to communicate with LLM engine at {self.base_url}")

    async def generate_chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.2,
    ) -> str:
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model_name,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": temperature,
            },
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload)
                if response.status_code != 200:
                    logger.error(f"Ollama chat failed ({response.status_code}): {response.text}")
                    raise AIInferenceException(
                        f"Ollama chat error: status code {response.status_code}"
                    )

                data = response.json()
                return data.get("message", {}).get("content", "").strip()
        except httpx.RequestError as e:
            logger.error(f"Network error in Ollama chat: {str(e)}")
            raise AIInferenceException("Failed to reach Ollama AI instance.")