import re
from typing import List, Set
from app.services.skill_extraction_service import SkillExtractionService


class ResumeSkillExtractor:
    """Extracts technical and soft skills from structured and unstructured resume sections."""

    @classmethod
    def extract_skills_from_text(cls, text: str) -> List[str]:
        """Scans resume text and returns canonical, lowercase skill names."""
        return SkillExtractionService.extract_from_text(text)

    @classmethod
    def extract_skills_from_section(cls, section_lines: List[str]) -> List[str]:
        """Extracts skills from identified 'Skills' resume sections."""
        combined_text = " , ".join(section_lines)
        # 1. Regex search across canonical lexicon
        extracted_canonical = SkillExtractionService.extract_from_text(combined_text)

        # 2. Tokenized comma/bullet parsing
        token_skills: Set[str] = set(extracted_canonical)
        delimiters = r"[,|•·\n\r/]"
        tokens = re.split(delimiters, combined_text)

        for token in tokens:
            cleaned = token.strip().lower()
            if cleaned and len(cleaned) <= 30:
                normalized = SkillExtractionService.normalize_skill(cleaned)
                if normalized:
                    token_skills.add(normalized)

        return sorted(list(token_skills))