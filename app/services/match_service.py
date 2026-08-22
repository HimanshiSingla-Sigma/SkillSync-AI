from typing import Dict, List, Set, Tuple
from app.models.student import StudentModel
from app.models.placement_drive import PlacementDriveModel


class MatchService:
    """
    Computes profile-to-job matching metrics, overlap sets, and missing skill analysis.
    Decoupled from deterministic eligibility verification.
    """

    @staticmethod
    def calculate_match_metrics(
        student_skills: List[str],
        required_skills: List[str],
    ) -> Tuple[float, List[str], List[str]]:
        """
        Calculates skill match percentage, matched skills list, and missing skills list.
        
        Formula:
            Match % = (Number of Matched Skills / Total Required Skills) * 100
            Returns 100.0% if no specific skills are required.
        """
        student_set: Set[str] = {s.strip().lower() for s in student_skills if s.strip()}
        required_set: Set[str] = {s.strip().lower() for s in required_skills if s.strip()}

        if not required_set:
            return 100.0, sorted(list(student_set)), []

        matched = student_set.intersection(required_set)
        missing = required_set.difference(student_set)

        match_pct = round((len(matched) / len(required_set)) * 100.0, 2)

        return match_pct, sorted(list(matched)), sorted(list(missing))

    @classmethod
    def evaluate_student_drive_match(
        cls,
        student: StudentModel,
        drive: PlacementDriveModel,
    ) -> Dict[str, any]:
        """Generates comprehensive matching profile for a student against a drive."""
        all_required = list(
            set(drive.required_skills + drive.eligibility_criteria.mandatory_skills)
        )
        match_pct, matched, missing = cls.calculate_match_metrics(
            student_skills=student.skills,
            required_skills=all_required,
        )

        return {
            "match_percentage": match_pct,
            "matched_skills": matched,
            "missing_skills": missing,
            "total_required_skills": len(all_required),
            "student_skill_count": len(student.skills),
        }