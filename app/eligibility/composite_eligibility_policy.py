from typing import List, Optional
from app.eligibility.base_policy import BaseEligibilityPolicy
from app.eligibility.cgpa_policy import CGPAPolicy
from app.eligibility.backlog_policy import BacklogPolicy
from app.eligibility.graduation_year_policy import GraduationYearPolicy
from app.eligibility.programme_policy import ProgrammePolicy
from app.eligibility.skill_policy import SkillPolicy
from app.eligibility.eligibility_result import EligibilityResultBuilder
from app.models.student import StudentModel
from app.models.placement_drive import PlacementDriveModel
from app.models.eligibility import EligibilityResultModel


class CompositeEligibilityPolicy:
    """
    Composite evaluator that executes a configurable pipeline of deterministic eligibility policies.
    Guarantees reproducible, audit-compliant outcomes.
    """

    def __init__(self, policies: Optional[List[BaseEligibilityPolicy]] = None):
        self.policies = policies or [
            CGPAPolicy(),
            BacklogPolicy(),
            GraduationYearPolicy(),
            ProgrammePolicy(),
            SkillPolicy(),
        ]

    def evaluate(
        self,
        student: StudentModel,
        drive: PlacementDriveModel,
    ) -> EligibilityResultModel:
        builder = EligibilityResultBuilder()

        for policy in self.policies:
            eval_result = policy.evaluate(student, drive)
            builder.add_evaluation(policy.policy_name, eval_result)

        return builder.build()