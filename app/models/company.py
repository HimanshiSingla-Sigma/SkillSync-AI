from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class CompanyModel(BaseModel):
    """Domain model representing an enterprise recruiter/company in MongoDB."""

    id: Optional[str] = Field(default=None, alias="_id")
    name: str = Field(..., description="Official Company Name")
    email: EmailStr = Field(..., description="Recruiter contact or company admin email")
    hashed_password: str
    role: str = Field(default="RECRUITER")
    is_active: bool = Field(default=True)

    industry: str = Field(default="Information Technology")
    website: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda dt: dt.isoformat()}