from app.eligibility.base_policy import BaseEligibilityPolicy
from app.models.student import StudentModel
from app.models.placement_drive import PlacementDriveModel
from app.models.eligibility import PolicyEvaluation


class CGPAPolicy(BaseEligibilityPolicy):
    """Evaluates whether the student meets the minimum required CGPA threshold."""

    @property
    def policy_name(self) -> str:
        return "cgpa"

    def evaluate(
        self,
        student: StudentModel,
        drive: PlacementDriveModel,
    ) -> PolicyEvaluation:
        min_cgpa = float(drive.eligibility_criteria.min_cgpa)
        student_cgpa = float(student.profile.cgpa)

        # A minimum threshold of 0.0 means no CGPA restriction is imposed
        if min_cgpa <= 0.0 or student_cgpa >= min_cgpa:
            return PolicyEvaluation(
                passed=True,
                status="PASS",
                message=f"Student CGPA ({student_cgpa:.2f}) meets or exceeds requirement ({min_cgpa:.2f}).",
                expected=f">= {min_cgpa:.2f}",
                actual=f"{student_cgpa:.2f}",
            )

        return PolicyEvaluation(
            passed=False,
            status="FAIL",
            message=f"Student CGPA ({student_cgpa:.2f}) is below minimum required ({min_cgpa:.2f}).",
            expected=f">= {min_cgpa:.2f}",
            actual=f"{student_cgpa:.2f}",
        )