from datetime import datetime, timezone
from typing import Optional, List
from pydantic import BaseModel, Field


class SkillModel(BaseModel):
    """Domain model representing a normalized technical or soft skill."""

    id: Optional[str] = Field(default=None, alias="_id")
    name: str = Field(..., description="Original raw skill name, e.g. Python 3")
    normalized_name: str = Field(
        ...,
        description="Canonical lowercased identifier, e.g. python",
    )
    category: str = Field(
        default="General",
        description="Skill domain: Programming, Cloud, Database, AI/ML, DevOps, SoftSkill",
    )
    aliases: List[str] = Field(
        default_factory=list,
        description="Synonyms or variations, e.g. ['py', 'python3', 'pythonscript']",
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda dt: dt.isoformat()}