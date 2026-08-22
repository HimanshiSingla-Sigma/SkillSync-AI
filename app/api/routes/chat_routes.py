from typing import Any, Dict, List
from fastapi import APIRouter, Depends
from app.ai.career_assistant_service import CareerAssistantService
from app.ai.faq_service import FAQService
from app.api.dependencies import get_current_user_id, require_student
from app.schemas.chat_schema import ChatMessageRequest, ChatMessageResponse

router = APIRouter(prefix="/chat", tags=["AI Career Assistant & GraphRAG"])
chat_service = CareerAssistantService()


@router.post(
    "/ask",
    response_model=ChatMessageResponse,
    dependencies=[Depends(require_student)],
)
async def ask_career_assistant(
    req: ChatMessageRequest, student_id: str = Depends(get_current_user_id)
):
    """
    GraphRAG Question Answering Endpoint:
    - User Question
    - Graph Traversal (Student profile, target drive, skill overlap, missing skills)
    - Deterministic context injection
    - LLM explanation generation (Constrained to knowledge graph facts)
    """
    return await chat_service.handle_chat_message(student_id, req)


@router.get("/faqs", response_model=List[Dict[str, str]])
async def get_placement_faqs():
    """Retrieves instant recruitment FAQs."""
    return FAQService.get_faqs()