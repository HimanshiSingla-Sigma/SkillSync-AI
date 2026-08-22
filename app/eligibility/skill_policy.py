from app.eligibility.base_policy import BaseEligibilityPolicy
from app.models.student import StudentModel
from app.models.placement_drive import PlacementDriveModel
from app.models.eligibility import PolicyEvaluation


class SkillPolicy(BaseEligibilityPolicy):
    """Evaluates mandatory skills that are strictly required for eligibility (distinct from match percentage)."""

    @property
    def policy_name(self) -> str:
        return "skills"

    def evaluate(
        self,
        student: StudentModel,
        drive: PlacementDriveModel,
    ) -> PolicyEvaluation:
        mandatory_skills = [
            s.strip().lower() for s in drive.eligibility_criteria.mandatory_skills if s.strip()
        ]
        student_skills = {s.strip().lower() for s in student.skills if s.strip()}

        # If no mandatory skills are configured, the policy passes automatically
        if not mandatory_skills:
            return PolicyEvaluation(
                passed=True,
                status="PASS",
                message="No mandatory skill requirements specified for eligibility.",
                expected="None",
                actual=f"{len(student_skills)} skills possessed",
            )

        missing_mandatory = [skill for skill in mandatory_skills if skill not in student_skills]

        if not missing_mandatory:
            return PolicyEvaluation(
                passed=True,
                status="PASS",
                message="Student possesses all mandatory required skills.",
                expected=str(mandatory_skills),
                actual=str(list(student_skills)),
            )

        return PolicyEvaluation(
            passed=False,
            status="FAIL",
            message=f"Missing mandatory required skills: {', '.join(missing_mandatory)}.",
            expected=str(mandatory_skills),
            actual=str(list(student_skills)),
        )