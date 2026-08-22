from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class ExtractedEducationSchema(BaseModel):
    degree: Optional[str] = None
    branch: Optional[str] = None
    university: Optional[str] = None
    graduation_year: Optional[int] = None
    cgpa: Optional[float] = None


class ExtractedProjectSchema(BaseModel):
    title: str
    description: Optional[str] = None
    technologies: List[str] = Field(default_factory=list)


class ExtractedExperienceSchema(BaseModel):
    company: str
    role: str
    duration: Optional[str] = None
    description: Optional[str] = None


class ResumeCorrectionRequest(BaseModel):
    extracted_name: Optional[str] = None
    extracted_email: Optional[str] = None
    extracted_phone: Optional[str] = None
    extracted_education: Optional[List[ExtractedEducationSchema]] = None
    extracted_skills: Optional[List[str]] = None
    extracted_projects: Optional[List[ExtractedProjectSchema]] = None
    extracted_experience: Optional[List[ExtractedExperienceSchema]] = None
    extracted_certifications: Optional[List[str]] = None


class ResumeResponse(BaseModel):
    id: str
    student_id: str
    file_name: str
    file_type: str
    raw_text: str
    extracted_name: Optional[str] = None
    extracted_email: Optional[str] = None
    extracted_phone: Optional[str] = None
    extracted_education: List[ExtractedEducationSchema]
    extracted_skills: List[str]
    extracted_projects: List[ExtractedProjectSchema]
    extracted_experience: List[ExtractedExperienceSchema]
    extracted_certifications: List[str]
    uploaded_at: datetime
    updated_at: datetime