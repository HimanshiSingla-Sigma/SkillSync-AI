from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class PolicyEvaluationDetail(BaseModel):
    passed: bool
    status: str
    message: str
    expected: Optional[str] = None
    actual: Optional[str] = None


class EligibilityCheckResponse(BaseModel):
    student_id: str
    drive_id: str
    eligible: bool
    criteria: Dict[str, str] = Field(
        ...,
        description="Key-value mapping of policy statuses: e.g. {'cgpa': 'PASS', 'skills': 'FAIL'}",
    )
    passed_criteria: List[str]
    failed_criteria: List[str]
    reasons: List[str]
    policy_details: Dict[str, PolicyEvaluationDetail]
    match_percentage: float
    matched_skills: List[str]
    missing_skills: List[str]