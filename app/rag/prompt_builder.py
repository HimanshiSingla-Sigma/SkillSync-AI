class PromptBuilder:
    """Assembles prompt templates strictly constraining LLM hallucination."""

    SYSTEM_INSTRUCTION = (
        "You are CareerConnect AI, an intelligent, objective college placement counselor. "
        "Your role is to explain eligibility, recommend preparation roadmaps, and assist students. "
        "CRITICAL RULES:\n"
        "1. Treat the provided Knowledge Graph & Database Context as GROUND TRUTH.\n"
        "2. NEVER override or contradict the deterministic eligibility verdict.\n"
        "3. NEVER invent or hallucinate required skills or policies not present in the context.\n"
        "4. Be encouraging, clear, and actionable in your guidance."
    )

    @classmethod
    def build_eligibility_explanation_prompt(
        cls,
        question: str,
        context_str: str,
    ) -> str:
        return (
            f"{context_str}\n\n"
            f"User Question: \"{question}\"\n\n"
            "Task: Provide a concise, clear explanation addressing the student's question based strictly "
            "on the context above. State clearly why they are eligible or ineligible, mention any missing "
            "skills, and advise them on what steps to take next."
        )

    @classmethod
    def build_career_advice_prompt(
        cls,
        question: str,
        context_str: str,
    ) -> str:
        return (
            f"{context_str}\n\n"
            f"User Question: \"{question}\"\n\n"
            "Task: Answer the student's question by analyzing the placement opportunities, highlighting "
            "their strengths, and giving actionable learning priorities for any missing skills."
        )