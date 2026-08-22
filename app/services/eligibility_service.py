from typing import Optional
from app.eligibility.composite_eligibility_policy import CompositeEligibilityPolicy
from app.models.student import StudentModel
from app.models.placement_drive import PlacementDriveModel
from app.models.eligibility import EligibilityResultModel
from app.services.match_service import MatchService
from app.schemas.eligibility_schema import EligibilityCheckResponse, PolicyEvaluationDetail
from app.repositories.student_repository import StudentRepository
from app.repositories.drive_repository import DriveRepository
from app.utils.exceptions import NotFoundException


class EligibilityService:
    """Unified service orchestrating rule-based eligibility evaluation and JD matching."""

    def __init__(
        self,
        student_repo: Optional[StudentRepository] = None,
        drive_repo: Optional[DriveRepository] = None,
        composite_policy: Optional[CompositeEligibilityPolicy] = None,
    ):
        self.student_repo = student_repo or StudentRepository()
        self.drive_repo = drive_repo or DriveRepository()
        self.policy_engine = composite_policy or CompositeEligibilityPolicy()

    async def check_eligibility(
        self,
        student_id: str,
        drive_id: str,
    ) -> EligibilityCheckResponse:
        """Evaluates student eligibility and profile match metrics for a placement drive."""
        student = await self.student_repo.find_by_id(student_id)
        if not student:
            raise NotFoundException(f"Student with ID '{student_id}' not found.")

        drive = await self.drive_repo.find_by_id(drive_id)
        if not drive:
            raise NotFoundException(f"Placement Drive with ID '{drive_id}' not found.")

        # 1. Deterministic Rule-Based Evaluation
        eligibility_result: EligibilityResultModel = self.policy_engine.evaluate(student, drive)

        # 2. Skill Match Metric Computation
        match_data = MatchService.evaluate_student_drive_match(student, drive)

        policy_details = {
            k: PolicyEvaluationDetail(
                passed=v.passed,
                status=v.status,
                message=v.message,
                expected=v.expected,
                actual=v.actual,
            )
            for k, v in eligibility_result.policy_details.items()
        }

        return EligibilityCheckResponse(
            student_id=str(student.id),
            drive_id=str(drive.id),
            eligible=eligibility_result.eligible,
            criteria=eligibility_result.criteria,
            passed_criteria=eligibility_result.passed_criteria,
            failed_criteria=eligibility_result.failed_criteria,
            reasons=eligibility_result.reasons,
            policy_details=policy_details,
            match_percentage=match_data["match_percentage"],
            matched_skills=match_data["matched_skills"],
            missing_skills=match_data["missing_skills"],
        )