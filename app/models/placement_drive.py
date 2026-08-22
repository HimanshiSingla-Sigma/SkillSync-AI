from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, Field


class DriveEligibilityCriteria(BaseModel):
    """Configurable deterministic rules defined by the recruiter."""

    min_cgpa: float = Field(default=0.0, ge=0.0, le=10.0)
    max_backlogs: int = Field(default=0, ge=0)
    allowed_programmes: List[str] = Field(
        default_factory=list,
        description="List of allowed branches/programmes e.g. ['B.Tech CSE', 'B.Tech IT']",
    )
    allowed_graduation_years: List[int] = Field(
        default_factory=list,
        description="Eligible batch passing years e.g. [2024, 2025]",
    )
    mandatory_skills: List[str] = Field(
        default_factory=list,
        description="Skills strictly required for deterministic eligibility",
    )


class PlacementDriveModel(BaseModel):
    """Domain model representing a recruitment drive posted by a company."""

    id: Optional[str] = Field(default=None, alias="_id")
    company_id: str = Field(..., description="Reference to Company._id")
    company_name: str = Field(..., description="Denormalized company name for fast search")
    title: str = Field(..., description="Job/Internship Title e.g. Software Development Engineer")
    role_type: str = Field(default="Full-Time", description="Full-Time, Internship, Contract")
    salary_package: str = Field(..., description="CTC or Stipend e.g. 12 LPA or 50,000/month")
    location: str = Field(default="Remote")
    job_description: str = Field(...)

    required_skills: List[str] = Field(
        default_factory=list,
        description="All target skills for match percentage calculation",
    )
    eligibility_criteria: DriveEligibilityCriteria = Field(
        default_factory=DriveEligibilityCriteria
    )

    status: str = Field(
        default="PUBLISHED",
        description="DRAFT, PUBLISHED, CLOSED, COMPLETED",
    )
    deadline: Optional[datetime] = None

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda dt: dt.isoformat()}