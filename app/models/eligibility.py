from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class PolicyEvaluation(BaseModel):
    """Individual policy evaluation result."""

    passed: bool
    status: str = Field(..., description="PASS or FAIL")
    message: str
    expected: Optional[str] = None
    actual: Optional[str] = None


class EligibilityResultModel(BaseModel):
    """Unified deterministic evaluation output for a student against a placement drive."""

    eligible: bool
    criteria: Dict[str, str] = Field(
        ...,
        description="Key-value mapping of policy status e.g. {'cgpa': 'PASS', 'skills': 'FAIL'}",
    )
    passed_criteria: List[str] = Field(default_factory=list)
    failed_criteria: List[str] = Field(default_factory=list)
    reasons: List[str] = Field(default_factory=list)
    policy_details: Dict[str, PolicyEvaluation] = Field(default_factory=dict)