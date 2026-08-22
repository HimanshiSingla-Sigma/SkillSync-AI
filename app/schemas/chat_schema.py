from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ChatMessageRequest(BaseModel):
    question: str = Field(..., min_length=2, description="Student career or eligibility query")
    drive_id: Optional[str] = Field(
        None, description="Contextual placement drive ID if inquiring about a specific company/drive"
    )


class ChatContextSnapshot(BaseModel):
    student_name: str
    student_skills: List[str]
    target_drive_title: Optional[str] = None
    target_company_name: Optional[str] = None
    required_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    is_eligible: Optional[bool] = None
    failed_reasons: List[str] = Field(default_factory=list)


class ChatMessageResponse(BaseModel):
    question: str
    answer: str
    retrieved_graph_context: Dict[str, Any]
    suggested_skills_to_learn: List[str] = Field(default_factory=list)
    recommended_drives: List[str] = Field(default_factory=list)