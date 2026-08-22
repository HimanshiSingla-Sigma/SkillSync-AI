from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field


class StudentProfile(BaseModel):
    """Academic and personal details for a student."""

    cgpa: float = Field(default=0.0, ge=0.0, le=10.0)
    backlogs: int = Field(default=0, ge=0)
    programme: str = Field(
        default="", description="Degree & Branch: e.g., B.Tech Computer Science"
    )
    branch: str = Field(default="", description="e.g., Computer Science")
    graduation_year: int = Field(default=2025)
    phone: Optional[str] = None
    bio: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None


class StudentModel(BaseModel):
    """Domain model representing a Student user in MongoDB."""

    id: Optional[str] = Field(default=None, alias="_id")
    email: EmailStr
    hashed_password: str
    full_name: str
    role: str = Field(default="STUDENT")
    is_active: bool = Field(default=True)

    profile: StudentProfile = Field(default_factory=StudentProfile)
    skills: List[str] = Field(
        default_factory=list,
        description="Normalized skill strings owned by the student",
    )
    resume_id: Optional[str] = Field(
        default=None, description="Reference to active Resume document"
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda dt: dt.isoformat()}