from typing import Optional
from app.rag.graph_rag_service import GraphRAGService
from app.schemas.chat_schema import ChatMessageRequest, ChatMessageResponse


class CareerAssistantService:
    """High-level facade unifying AI queries, eligibility reasoning, and GraphRAG operations."""

    def __init__(self, rag_service: Optional[GraphRAGService] = None):
        self.rag_service = rag_service or GraphRAGService()

    async def handle_chat_message(
        self,
        student_id: str,
        request: ChatMessageRequest,
    ) -> ChatMessageResponse:
        return await self.rag_service.process_student_query(
            student_id=student_id,
            question=request.question,
            drive_id=request.drive_id,
        )