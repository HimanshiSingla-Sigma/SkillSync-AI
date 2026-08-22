import re
from typing import List, Optional
from app.services.skill_extraction_service import SkillExtractionService


class ResumeNormalizer:
    """Cleans, strips, and formats extracted resume entities into standardized data."""

    @staticmethod
    def clean_text(raw_text: str) -> str:
        """Removes null bytes, excessive white spaces, and non-printable characters."""
        if not raw_text:
            return ""
        cleaned = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]", " ", raw_text)
        cleaned = re.sub(r"[ \t]+", " ", cleaned)
        cleaned = re.sub(r"\n\s*\n", "\n", cleaned)
        return cleaned.strip()

    @staticmethod
    def normalize_phone(phone_str: Optional[str]) -> Optional[str]:
        """Formats phone numbers by stripping extra punctuation and characters."""
        if not phone_str:
            return None
        digits_only = re.sub(r"[^\d+]", "", phone_str)
        if len(digits_only) >= 10:
            return digits_only
        return phone_str.strip()

    @staticmethod
    def normalize_email(email_str: Optional[str]) -> Optional[str]:
        """Converts email string to trimmed lowercase."""
        if not email_str:
            return None
        return email_str.strip().lower()

    @staticmethod
    def normalize_skills(skills: List[str]) -> List[str]:
        """Passes skill items through canonical mapping."""
        return SkillExtractionService.extract_and_normalize(skills)