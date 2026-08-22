from typing import Dict, List, Set, Tuple
from app.matching.percentage_calculator import PercentageCalculator


class SkillMatcher:
    """Performs set-based skill comparisons and identifies skill gaps."""

    @classmethod
    def match(
        cls,
        candidate_skills: List[str],
        required_skills: List[str],
    ) -> Dict[str, any]:
        """Calculates match score, matched items, and missing skills."""
        cand_set: Set[str] = {s.strip().lower() for s in candidate_skills if s.strip()}
        req_set: Set[str] = {s.strip().lower() for s in required_skills if s.strip()}

        matched = cand_set.intersection(req_set)
        missing = req_set.difference(cand_set)
        score = PercentageCalculator.calculate_skill_overlap_score(candidate_skills, required_skills)

        return {
            "match_percentage": score,
            "matched_skills": sorted(list(matched)),
            "missing_skills": sorted(list(missing)),
            "total_required": len(req_set),
            "total_candidate": len(cand_set),
        }