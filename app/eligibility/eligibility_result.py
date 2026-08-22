from typing import Dict, List
from app.models.eligibility import EligibilityResultModel, PolicyEvaluation


class EligibilityResultBuilder:
    """Helper factory for assembling structured, validated EligibilityResultModel instances."""

    def __init__(self):
        self.criteria: Dict[str, str] = {}
        self.passed_criteria: List[str] = []
        self.failed_criteria: List[str] = []
        self.reasons: List[str] = []
        self.policy_details: Dict[str, PolicyEvaluation] = {}

    def add_evaluation(self, policy_name: str, evaluation: PolicyEvaluation) -> "EligibilityResultBuilder":
        self.criteria[policy_name] = evaluation.status
        self.policy_details[policy_name] = evaluation

        if evaluation.passed:
            self.passed_criteria.append(policy_name)
        else:
            self.failed_criteria.append(policy_name)
            self.reasons.append(evaluation.message)

        return self

    def build(self) -> EligibilityResultModel:
        is_eligible = len(self.failed_criteria) == 0
        return EligibilityResultModel(
            eligible=is_eligible,
            criteria=self.criteria,
            passed_criteria=self.passed_criteria,
            failed_criteria=self.failed_criteria,
            reasons=self.reasons,
            policy_details=self.policy_details,
        )