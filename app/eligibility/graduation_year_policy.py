from app.eligibility.base_policy import BaseEligibilityPolicy
from app.models.student import StudentModel
from app.models.placement_drive import PlacementDriveModel
from app.models.eligibility import PolicyEvaluation


class GraduationYearPolicy(BaseEligibilityPolicy):
    """Evaluates whether the student's passing out batch/year is eligible for the recruitment drive."""

    @property
    def policy_name(self) -> str:
        return "graduation_year"

    def evaluate(
        self,
        student: StudentModel,
        drive: PlacementDriveModel,
    ) -> PolicyEvaluation:
        allowed_years = drive.eligibility_criteria.allowed_graduation_years
        student_year = int(student.profile.graduation_year)

        # Empty allowed_years implies all batches/years are permitted
        if not allowed_years or student_year in allowed_years:
            return PolicyEvaluation(
                passed=True,
                status="PASS",
                message=f"Graduation year ({student_year}) is eligible.",
                expected=str(allowed_years) if allowed_years else "Any",
                actual=str(student_year),
            )

        return PolicyEvaluation(
            passed=False,
            status="FAIL",
            message=f"Graduation year ({student_year}) is not in allowed batches: {allowed_years}.",
            expected=str(allowed_years),
            actual=str(student_year),
        )