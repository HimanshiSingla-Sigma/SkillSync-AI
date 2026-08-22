from typing import List, Optional
from app.rag.graph_rag_service import GraphRAGService
from app.schemas.chat_schema import ChatMessageResponse


class PreparationGuidanceService:
    """Specialized AI service generating targeted preparation and skill learning roadmaps."""

    def __init__(self, rag_service: Optional[GraphRAGService] = None):
        self.rag_service = rag_service or GraphRAGService()

    async def generate_roadmap(
        self,
        student_id: str,
        drive_id: Optional[str] = None,
    ) -> ChatMessageResponse:
        question = (
            "What specific skills and technical concepts should I learn to maximize my placement chances?"
        )
        return await self.rag_service.process_student_query(
            student_id=student_id,
            question=question,
            drive_id=drive_id,
        )