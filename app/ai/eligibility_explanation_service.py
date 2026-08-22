from typing import Optional
from app.rag.graph_rag_service import GraphRAGService
from app.schemas.chat_schema import ChatMessageResponse


class EligibilityExplanationService:
    """Specialized AI assistant service focused on explaining eligibility results."""

    def __init__(self, rag_service: Optional[GraphRAGService] = None):
        self.rag_service = rag_service or GraphRAGService()

    async def explain_eligibility(
        self,
        student_id: str,
        drive_id: str,
        custom_question: Optional[str] = None,
    ) -> ChatMessageResponse:
        q = custom_question or "Why am I not eligible for this placement drive, and what are my missing requirements?"
        return await self.rag_service.process_student_query(
            student_id=student_id,
            question=q,
            drive_id=drive_id,
        )