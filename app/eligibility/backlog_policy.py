from app.eligibility.base_policy import BaseEligibilityPolicy
from app.models.student import StudentModel
from app.models.placement_drive import PlacementDriveModel
from app.models.eligibility import PolicyEvaluation


class BacklogPolicy(BaseEligibilityPolicy):
    """Evaluates whether the student's active backlog count is within allowable limits."""

    @property
    def policy_name(self) -> str:
        return "backlogs"

    def evaluate(
        self,
        student: StudentModel,
        drive: PlacementDriveModel,
    ) -> PolicyEvaluation:
        max_allowed = int(drive.eligibility_criteria.max_backlogs)
        student_backlogs = int(student.profile.backlogs)

        if student_backlogs <= max_allowed:
            return PolicyEvaluation(
                passed=True,
                status="PASS",
                message=f"Active backlogs ({student_backlogs}) are within the allowable limit (<= {max_allowed}).",
                expected=f"<= {max_allowed}",
                actual=f"{student_backlogs}",
            )

        return PolicyEvaluation(
            passed=False,
            status="FAIL",
            message=f"Active backlogs ({student_backlogs}) exceed the allowable limit ({max_allowed}).",
            expected=f"<= {max_allowed}",
            actual=f"{student_backlogs}",
        )