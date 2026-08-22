import re
from typing import Any, Dict, List, Optional
from app.models.resume import ExtractedEducation, ExtractedProject, ExtractedExperience
from app.resume_processing.skill_extractor import ResumeSkillExtractor
from app.resume_processing.resume_normalizer import ResumeNormalizer


class InformationExtractor:
    """Heuristic and regex parser for personal info, education, projects, and work history."""

    EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    PHONE_REGEX = r"(?:(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\+?\d{10,12})"
    CGPA_REGEX = r"(?:cgpa|gpa|percentage|pointer)[\s:]*([0-9]{1,2}(?:\.[0-9]{1,2})?)(?:\s*(?:/|out of)\s*(?:10|100|4))?"
    GRAD_YEAR_REGEX = r"\b(20[12][0-9])\b"

    @classmethod
    def extract_name(cls, lines: List[str]) -> Optional[str]:
        """Extracts candidate name assuming top lines contain full name."""
        for line in lines[:5]:
            line_clean = line.strip()
            if not line_clean:
                continue
            # Skip header labels, emails, phones, or URLs
            if re.search(cls.EMAIL_REGEX, line_clean) or re.search(cls.PHONE_REGEX, line_clean):
                continue
            if any(h in line_clean.lower() for h in ["resume", "curriculum vitae", "cv", "page"]):
                continue
            if 2 <= len(line_clean.split()) <= 4 and all(part.isalpha() for part in line_clean.split()):
                return line_clean
        return None

    @classmethod
    def extract_email(cls, text: str) -> Optional[str]:
        match = re.search(cls.EMAIL_REGEX, text)
        return ResumeNormalizer.normalize_email(match.group(0)) if match else None

    @classmethod
    def extract_phone(cls, text: str) -> Optional[str]:
        match = re.search(cls.PHONE_REGEX, text)
        return ResumeNormalizer.normalize_phone(match.group(0)) if match else None

    @classmethod
    def extract_education(cls, text: str) -> List[ExtractedEducation]:
        education_list: List[ExtractedEducation] = []
        degree_patterns = [
            (r"(?i)\b(b\.?tech(?:nology)?|b\.?e\.?|bachelor of technology|bachelor of engineering)\b", "B.Tech"),
            (r"(?i)\b(m\.?tech(?:nology)?|m\.?e\.?|master of technology)\b", "M.Tech"),
            (r"(?i)\b(b\.?c\.?a\.?|bachelor of computer applications)\b", "BCA"),
            (r"(?i)\b(m\.?c\.?a\.?|master of computer applications)\b", "MCA"),
            (r"(?i)\b(b\.?s\.?c\.?|bachelor of science)\b", "B.Sc"),
            (r"(?i)\b(m\.?s\.?c\.?|master of science)\b", "M.Sc"),
        ]

        branch_patterns = [
            (r"(?i)(computer science(?: and engineering)?|cse|cs)", "Computer Science"),
            (r"(?i)(information technology|it)", "Information Technology"),
            (r"(?i)(electronics and communication(?: engineering)?|ece)", "Electronics & Communication"),
            (r"(?i)(mechanical engineering|me)", "Mechanical Engineering"),
            (r"(?i)(data science|artificial intelligence|ai & ds)", "Data Science & AI"),
        ]

        for deg_regex, deg_name in degree_patterns:
            if re.search(deg_regex, text):
                detected_branch = "Computer Science"
                for br_regex, br_name in branch_patterns:
                    if re.search(br_regex, text):
                        detected_branch = br_name
                        break

                cgpa_match = re.search(cls.CGPA_REGEX, text, re.IGNORECASE)
                parsed_cgpa = float(cgpa_match.group(1)) if cgpa_match else None
                if parsed_cgpa and parsed_cgpa > 10.0:  # Normalized percentage scale
                    parsed_cgpa = round(parsed_cgpa / 10.0, 2)

                year_matches = re.findall(cls.GRAD_YEAR_REGEX, text)
                grad_year = int(year_matches[-1]) if year_matches else None

                education_list.append(
                    ExtractedEducation(
                        degree=deg_name,
                        branch=detected_branch,
                        university="University Institute of Technology",
                        graduation_year=grad_year or 2025,
                        cgpa=parsed_cgpa or 8.0,
                    )
                )
                break

        return education_list

    @classmethod
    def extract_structured_sections(cls, full_text: str) -> Dict[str, Any]:
        """Parses structured entities across all resume sections."""
        clean_text = ResumeNormalizer.clean_text(full_text)
        lines = [line.strip() for line in clean_text.split("\n") if line.strip()]

        name = cls.extract_name(lines)
        email = cls.extract_email(clean_text)
        phone = cls.extract_phone(clean_text)
        education = cls.extract_education(clean_text)
        skills = ResumeSkillExtractor.extract_skills_from_text(clean_text)

        # Basic Project & Experience identification
        projects = []
        experiences = []
        for i, line in enumerate(lines):
            if "project" in line.lower() and len(line) < 40 and i + 1 < len(lines):
                projects.append(
                    ExtractedProject(
                        title=line.replace(":", "").strip(),
                        description=lines[i + 1],
                        technologies=ResumeSkillExtractor.extract_skills_from_text(lines[i + 1]),
                    )
                )
            if any(k in line.lower() for k in ["intern", "experience", "developer"]) and len(line) < 50 and i + 1 < len(lines):
                experiences.append(
                    ExtractedExperience(
                        company=line.strip(),
                        role="Software Engineer Intern",
                        duration="Summer Internship",
                        description=lines[i + 1],
                    )
                )

        return {
            "name": name,
            "email": email,
            "phone": phone,
            "education": education,
            "skills": skills,
            "projects": projects[:5],
            "experience": experiences[:5],
            "certifications": [],
        }