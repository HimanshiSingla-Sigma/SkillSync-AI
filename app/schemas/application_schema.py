from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ApplicationCreateRequest(BaseModel):
    drive_id: str = Field(..., description="Placement Drive ID to apply for")


class ApplicationStatusUpdateRequest(BaseModel):
    status: str = Field(
        ...,
        description="PENDING, UNDER_REVIEW, SHORTLISTED, ASSESSMENT, INTERVIEW, SELECTED, REJECTED",
    )
    remarks: Optional[str] = Field(None, description="Optional reviewer remarks")


class ApplicationStatusHistoryResponse(BaseModel):
    status: str
    updated_by: str
    remarks: Optional[str] = None
    timestamp: datetime


class ApplicationResponse(BaseModel):
    id: str
    student_id: str
    drive_id: str
    company_id: str
    status: str
    status_history: List[ApplicationStatusHistoryResponse]
    match_percentage: float
    matched_skills: List[str]
    missing_skills: List[str]
    eligibility_snapshot: Dict[str, Any]
    created_at: datetime
    updated_at: datetime


class ApplicationDetailedResponse(BaseModel):
    id: str
    student_id: str
    student_name: str
    student_email: str
    student_cgpa: float
    student_branch: str
    drive_id: str
    drive_title: str
    company_id: str
    company_name: str
    status: str
    status_history: List[ApplicationStatusHistoryResponse]
    match_percentage: float
    matched_skills: List[str]
    missing_skills: List[str]
    created_at: datetime