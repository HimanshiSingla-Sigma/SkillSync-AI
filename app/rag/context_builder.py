from typing import Any, Dict, List, Optional


class ContextBuilder:
    """Transforms raw graph retrieval outputs into structured LLM context strings."""

    @staticmethod
    def build_student_drive_context(
        graph_data: Dict[str, Any],
        deterministic_eligibility: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Constructs an authoritative context block for student eligibility queries."""
        if not graph_data:
            return "No matching student or placement drive records found in the knowledge graph."

        student_name = graph_data.get("student_name", "Student")
        cgpa = graph_data.get("student_cgpa", 0.0)
        backlogs = graph_data.get("student_backlogs", 0)
        programme = graph_data.get("student_programme", "N/A")
        student_skills = ", ".join(graph_data.get("student_skills", [])) or "None recorded"

        drive_title = graph_data.get("drive_title", "Placement Drive")
        company = graph_data.get("company_name", "Company")
        min_cgpa = graph_data.get("min_cgpa", 0.0)
        max_backlogs = graph_data.get("max_backlogs", 0)
        allowed_progs = ", ".join(graph_data.get("allowed_programmes", [])) or "All"
        required_skills = ", ".join(graph_data.get("required_skills", [])) or "None"
        matched_skills = ", ".join(graph_data.get("matched_skills", [])) or "None"
        missing_skills = ", ".join(graph_data.get("missing_skills", [])) or "None"

        lines = [
            "--- AUTHORITATIVE KNOWLEDGE GRAPH & DATABASE CONTEXT ---",
            f"Candidate: {student_name}",
            f"Academic Profile: CGPA = {cgpa}, Active Backlogs = {backlogs}, Programme = {programme}",
            f"Possessed Skills: [{student_skills}]",
            "",
            f"Target Opportunity: {drive_title} at {company}",
            f"Eligibility Thresholds: Min CGPA = {min_cgpa}, Max Backlogs = {max_backlogs}, Allowed Programmes = [{allowed_progs}]",
            f"Required Job Skills: [{required_skills}]",
            f"Current Skill Overlap (Matched): [{matched_skills}]",
            f"Skill Gaps (Missing): [{missing_skills}]",
        ]

        if deterministic_eligibility:
            lines.extend([
                "",
                "DETERMINISTIC ELIGIBILITY ENGINE VERDICT (ABSOLUTE TRUTH):",
                f"- Eligible: {deterministic_eligibility.get('eligible')}",
                f"- Failed Rules: {deterministic_eligibility.get('failed_criteria', [])}",
                f"- Exact Reasons: {deterministic_eligibility.get('reasons', [])}",
            ])

        lines.append("---------------------------------------------------------")
        return "\n".join(lines)

    @staticmethod
    def build_recommendations_context(
        student_data: Dict[str, Any],
        drives_data: List[Dict[str, Any]],
    ) -> str:
        """Constructs context for job recommendations and career queries."""
        student_name = student_data.get("full_name", "Student")
        student_skills = ", ".join(student_data.get("skills", [])) or "None"

        lines = [
            "--- AUTHORITATIVE KNOWLEDGE GRAPH CONTEXT ---",
            f"Student: {student_name}",
            f"Academics: CGPA {student_data.get('cgpa')}, Backlogs {student_data.get('backlogs')}",
            f"Skills: [{student_skills}]",
            "",
            "AVAILABLE MATCHING PLACEMENT DRIVES:",
        ]

        for i, d in enumerate(drives_data, start=1):
            lines.append(
                f"{i}. {d.get('drive_title')} at {d.get('company_name')} | "
                f"Package: {d.get('salary_package')} | Match: {d.get('match_pct', 0):.1f}% | "
                f"Missing Skills: [{', '.join(d.get('missing_skills', []))}]"
            )

        lines.append("---------------------------------------------")
        return "\n".join(lines)