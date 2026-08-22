from app.eligibility.base_policy import BaseEligibilityPolicy
from app.models.student import StudentModel
from app.models.placement_drive import PlacementDriveModel
from app.models.eligibility import PolicyEvaluation


class ProgrammePolicy(BaseEligibilityPolicy):
    """Evaluates whether the student's academic degree/branch matches allowable drive programmes."""

    @property
    def policy_name(self) -> str:
        return "programme"

    def evaluate(
        self,
        student: StudentModel,
        drive: PlacementDriveModel,
    ) -> PolicyEvaluation:
        allowed_programmes = [p.strip().lower() for p in drive.eligibility_criteria.allowed_programmes if p.strip()]
        student_programme = student.profile.programme.strip().lower()
        student_branch = student.profile.branch.strip().lower()

        # If no programme restrictions are defined, allow all
        if not allowed_programmes:
            return PolicyEvaluation(
                passed=True,
                status="PASS",
                message="All academic programmes and branches are eligible.",
                expected="Any",
                actual=student.profile.programme or "Unspecified",
            )

        # Match either the full programme string or the specific branch
        is_match = any(
            allowed in student_programme or student_programme in allowed or allowed == student_branch
            for allowed in allowed_programmes
        )

        if is_match:
            return PolicyEvaluation(
                passed=True,
                status="PASS",
                message=f"Programme '{student.profile.programme}' matches eligible criteria.",
                expected=str(drive.eligibility_criteria.allowed_programmes),
                actual=student.profile.programme,
            )

        return PolicyEvaluation(
            passed=False,
            status="FAIL",
            message=f"Programme '{student.profile.programme}' is not eligible for this drive.",
            expected=str(drive.eligibility_criteria.allowed_programmes),
            actual=student.profile.programme,
        )