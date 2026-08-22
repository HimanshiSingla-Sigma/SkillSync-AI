from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class BaseLLMClient(ABC):
    """
    Abstract interface for LLM integrations.
    Decouples application logic from specific LLM providers (Ollama, OpenAI, vLLM, etc.).
    """

    @abstractmethod
    async def generate_response(
        self,
        prompt: str,
        system_instruction: Optional[str] = None,
        temperature: float = 0.2,
    ) -> str:
        """Generates a text completion given a prompt and optional system instructions."""
        pass

    @abstractmethod
    async def generate_chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.2,
    ) -> str:
        """Executes a multi-turn chat completion."""
        pass