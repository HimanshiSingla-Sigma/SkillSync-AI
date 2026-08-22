from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class CompanyRegisterRequest(BaseModel):
    name: str = Field(..., min_length=2, description="Company official name")
    email: EmailStr = Field(..., description="Company recruiter/admin email")
    password: str = Field(..., min_length=6, description="Plain text password")
    industry: str = Field(default="Information Technology")
    website: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    otp: Optional[str] = None


class CompanyLoginRequest(BaseModel):
    email: EmailStr
    password: str


class CompanyUpdateRequest(BaseModel):
    name: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None


class CompanyResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str
    is_active: bool
    industry: str
    website: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    created_at: datetime
    updated_at: datetime


class CompanyAuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    company: CompanyResponse