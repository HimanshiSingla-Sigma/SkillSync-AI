from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class DriveEligibilityCriteriaSchema(BaseModel):
    min_cgpa: float = Field(default=0.0, ge=0.0, le=10.0)
    max_backlogs: int = Field(default=0, ge=0)
    allowed_programmes: List[str] = Field(
        default_factory=list,
        description="e.g. ['B.Tech Computer Science', 'B.Tech IT']",
    )
    allowed_graduation_years: List[int] = Field(
        default_factory=list,
        description="e.g. [2024, 2025]",
    )
    mandatory_skills: List[str] = Field(
        default_factory=list,
        description="Strict deterministic skill requirements",
    )


class DriveCreateRequest(BaseModel):
    title: str = Field(..., min_length=2, description="e.g. Graduate Software Engineer")
    role_type: str = Field(default="Full-Time", description="Full-Time, Internship, Contract")
    salary_package: str = Field(..., description="e.g. 14 LPA")
    location: str = Field(default="Hybrid")
    job_description: str = Field(..., min_length=10)
    required_skills: List[str] = Field(
        default_factory=list,
        description="All targeted skills for match score calculations",
    )
    eligibility_criteria: DriveEligibilityCriteriaSchema = Field(
        default_factory=DriveEligibilityCriteriaSchema
    )
    deadline: Optional[datetime] = None


class DriveUpdateRequest(BaseModel):
    title: Optional[str] = None
    role_type: Optional[str] = None
    salary_package: Optional[str] = None
    location: Optional[str] = None
    job_description: Optional[str] = None
    required_skills: Optional[List[str]] = None
    eligibility_criteria: Optional[DriveEligibilityCriteriaSchema] = None
    status: Optional[str] = Field(None, description="DRAFT, PUBLISHED, CLOSED, COMPLETED")
    deadline: Optional[datetime] = None


class DriveResponse(BaseModel):
    id: str
    company_id: str
    company_name: str
    title: str
    role_type: str
    salary_package: str
    location: str
    job_description: str
    required_skills: List[str]
    eligibility_criteria: DriveEligibilityCriteriaSchema
    status: str
    deadline: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime