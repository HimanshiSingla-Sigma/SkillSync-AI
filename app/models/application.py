from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ApplicationStatus:
    PENDING = "PENDING"
    UNDER_REVIEW = "UNDER_REVIEW"
    SHORTLISTED = "SHORTLISTED"
    ASSESSMENT = "ASSESSMENT"
    INTERVIEW = "INTERVIEW"
    SELECTED = "SELECTED"
    REJECTED = "REJECTED"

    ALL = [
        PENDING,
        UNDER_REVIEW,
        SHORTLISTED,
        ASSESSMENT,
        INTERVIEW,
        SELECTED,
        REJECTED,
    ]


class ApplicationStatusHistory(BaseModel):
    status: str
    updated_by: str
    remarks: Optional[str] = None
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class ApplicationModel(BaseModel):
    """Domain model representing a student application to a placement drive."""

    id: Optional[str] = Field(default=None, alias="_id")
    student_id: str = Field(..., description="Reference to Student._id")
    drive_id: str = Field(..., description="Reference to PlacementDrive._id")
    company_id: str = Field(..., description="Reference to Company._id")

    status: str = Field(default=ApplicationStatus.PENDING)
    status_history: List[ApplicationStatusHistory] = Field(default_factory=list)

    # Snapshot of eligibility & match metrics at time of application
    match_percentage: float = Field(default=0.0)
    matched_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    eligibility_snapshot: Dict[str, Any] = Field(default_factory=dict)

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda dt: dt.isoformat()}