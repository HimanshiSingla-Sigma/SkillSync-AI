from abc import ABC, abstractmethod
from typing import Optional
from app.models.student import StudentModel
from app.models.placement_drive import PlacementDriveModel
from app.models.eligibility import PolicyEvaluation


class BaseEligibilityPolicy(ABC):
    """
    Abstract Base Class for deterministic, rule-based placement eligibility policies.
    LLMs are strictly prohibited from evaluating or overriding eligibility decisions.
    """

    @property
    @abstractmethod
    def policy_name(self) -> str:
        """Returns the unique programmatic identifier for the policy."""
        pass

    @abstractmethod
    def evaluate(
        self,
        student: StudentModel,
        drive: PlacementDriveModel,
    ) -> PolicyEvaluation:
        """
        Executes deterministic evaluation against a Student and a Placement Drive.
        
        Returns:
            PolicyEvaluation: Encapsulates pass/fail boolean, status string, 
                             diagnostic message, expected threshold, and actual value.
        """
        pass