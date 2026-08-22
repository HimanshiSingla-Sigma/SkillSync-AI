from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ExtractedEducation(BaseModel):
    degree: Optional[str] = None
    branch: Optional[str] = None
    university: Optional[str] = None
    graduation_year: Optional[int] = None
    cgpa: Optional[float] = None


class ExtractedProject(BaseModel):
    title: str
    description: Optional[str] = None
    technologies: List[str] = Field(default_factory=list)


class ExtractedExperience(BaseModel):
    company: str
    role: str
    duration: Optional[str] = None
    description: Optional[str] = None


class ResumeModel(BaseModel):
    """Domain model representing an uploaded and parsed resume document."""

    id: Optional[str] = Field(default=None, alias="_id")
    student_id: str = Field(..., description="Foreign key to Student._id")
    file_name: str
    file_path: str
    file_type: str = Field(..., description="pdf or docx")
    raw_text: str = Field(default="", description="Extracted raw text content")

    # Structured extractions
    extracted_name: Optional[str] = None
    extracted_email: Optional[str] = None
    extracted_phone: Optional[str] = None
    extracted_education: List[ExtractedEducation] = Field(default_factory=list)
    extracted_skills: List[str] = Field(default_factory=list)
    extracted_projects: List[ExtractedProject] = Field(default_factory=list)
    extracted_experience: List[ExtractedExperience] = Field(default_factory=list)
    extracted_certifications: List[str] = Field(default_factory=list)

    parsing_metadata: Dict[str, Any] = Field(default_factory=dict)
    uploaded_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda dt: dt.isoformat()}