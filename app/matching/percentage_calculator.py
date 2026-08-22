from typing import List, Set


class PercentageCalculator:
    """Calculates deterministic numerical matching scores."""

    @staticmethod
    def calculate_skill_overlap_score(
        candidate_skills: List[str],
        required_skills: List[str],
    ) -> float:
        """Computes overlap fraction: (len(candidate ∩ required) / len(required)) * 100."""
        cand_set: Set[str] = {s.strip().lower() for s in candidate_skills if s.strip()}
        req_set: Set[str] = {s.strip().lower() for s in required_skills if s.strip()}

        if not req_set:
            return 100.0

        matched_count = len(cand_set.intersection(req_set))
        score = (matched_count / len(req_set)) * 100.0
        return round(score, 2)

    @staticmethod
    def calculate_weighted_match(
        skill_score: float,
        cgpa_score: float,
        skill_weight: float = 0.8,
        cgpa_weight: float = 0.2,
    ) -> float:
        """Computes combined multi-factor weighted match score."""
        weighted = (skill_score * skill_weight) + (cgpa_score * cgpa_weight)
        return round(min(100.0, max(0.0, weighted)), 2)