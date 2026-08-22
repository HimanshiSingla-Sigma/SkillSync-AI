from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field


class StudentProfileUpdate(BaseModel):
    cgpa: Optional[float] = Field(None, ge=0.0, le=10.0, description="Cumulative Grade Point Average")
    backlogs: Optional[int] = Field(None, ge=0, description="Active backlog count")
    programme: Optional[str] = Field(None, description="e.g., B.Tech Computer Science")
    branch: Optional[str] = Field(None, description="e.g., Computer Science")
    graduation_year: Optional[int] = Field(None, ge=2000, le=2050)
    phone: Optional[str] = Field(None, description="Contact phone number")
    bio: Optional[str] = Field(None, description="Short personal bio")
    github_url: Optional[str] = Field(None, description="GitHub profile URL")
    linkedin_url: Optional[str] = Field(None, description="LinkedIn profile URL")


class StudentProfileResponse(BaseModel):
    cgpa: float = 0.0
    backlogs: int = 0
    programme: str = ""
    branch: str = ""
    graduation_year: int = 2025
    phone: Optional[str] = None
    bio: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None


class StudentRegisterRequest(BaseModel):
    email: EmailStr = Field(..., description="Student university or personal email")
    password: str = Field(..., min_length=6, description="Plain text password")
    full_name: str = Field(..., min_length=2, description="Student full name")
    cgpa: float = Field(default=0.0, ge=0.0, le=10.0)
    backlogs: int = Field(default=0, ge=0)
    programme: str = Field(default="B.Tech Computer Science")
    branch: str = Field(default="Computer Science")
    graduation_year: int = Field(default=2025)
    skills: List[str] = Field(default_factory=list)
    otp: Optional[str] = None


class StudentLoginRequest(BaseModel):
    email: EmailStr
    password: str


class StudentUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    profile: Optional[StudentProfileUpdate] = None
    skills: Optional[List[str]] = None
    cgpa: Optional[float] = None
    backlogs: Optional[int] = None
    programme: Optional[str] = None
    branch: Optional[str] = None
    graduation_year: Optional[int] = None


class StudentSkillsUpdateRequest(BaseModel):
    skills: List[str] = Field(..., description="Full updated list of skill names")


class StudentResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    role: str
    is_active: bool
    profile: StudentProfileResponse
    skills: List[str]
    resume_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class StudentAuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    student: StudentResponse