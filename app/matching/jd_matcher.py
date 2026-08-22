from typing import Any, Dict
from app.models.student import StudentModel
from app.models.placement_drive import PlacementDriveModel
from app.matching.skill_matcher import SkillMatcher
from app.matching.percentage_calculator import PercentageCalculator
from app.resume_processing.skill_extractor import ResumeSkillExtractor


class JDMatcher:
    """Matches candidate profile against parsed Job Descriptions."""

    @classmethod
    def match_student_to_drive(
        cls,
        student: StudentModel,
        drive: PlacementDriveModel,
    ) -> Dict[str, Any]:
        """Extracts skills from JD and computes overall match against student skills."""
        # 1. Collect skills from drive definition and raw JD text
        drive_skills = set(drive.required_skills + drive.eligibility_criteria.mandatory_skills)
        extracted_from_jd = ResumeSkillExtractor.extract_skills_from_text(drive.job_description)
        all_required = list(drive_skills.union(extracted_from_jd))

        # 2. Skill match
        skill_res = SkillMatcher.match(student.skills, all_required)

        # 3. CGPA scoring component (10 CGPA = 100%)
        cgpa_score = min(100.0, (student.profile.cgpa / 10.0) * 100.0)
        overall_match = PercentageCalculator.calculate_weighted_match(
            skill_score=skill_res["match_percentage"],
            cgpa_score=cgpa_score,
            skill_weight=0.85,
            cgpa_weight=0.15,
        )

        return {
            "overall_match_percentage": overall_match,
            "skill_match_percentage": skill_res["match_percentage"],
            "matched_skills": skill_res["matched_skills"],
            "missing_skills": skill_res["missing_skills"],
            "all_required_skills": all_required,
        }