from typing import Any, Dict, Optional
from app.models.student import StudentModel
from app.models.placement_drive import PlacementDriveModel
from app.eligibility.composite_eligibility_policy import CompositeEligibilityPolicy
from app.matching.jd_matcher import JDMatcher


class EligibilityMatcher:
    """Combines rule-based eligibility evaluation with match percentage calculations."""

    def __init__(self, policy_engine: Optional[CompositeEligibilityPolicy] = None):
        self.policy_engine = policy_engine or CompositeEligibilityPolicy()

    def evaluate_all(
        self,
        student: StudentModel,
        drive: PlacementDriveModel,
    ) -> Dict[str, Any]:
        """Calculates both deterministic eligibility and profile match scores."""
        # 1. Deterministic eligibility
        eligibility_result = self.policy_engine.evaluate(student, drive)

        # 2. Profile matching
        match_result = JDMatcher.match_student_to_drive(student, drive)

        return {
            "eligible": eligibility_result.eligible,
            "criteria": eligibility_result.criteria,
            "failed_criteria": eligibility_result.failed_criteria,
            "passed_criteria": eligibility_result.passed_criteria,
            "reasons": eligibility_result.reasons,
            "match_percentage": match_result["skill_match_percentage"],
            "overall_match_percentage": match_result["overall_match_percentage"],
            "matched_skills": match_result["matched_skills"],
            "missing_skills": match_result["missing_skills"],
        }