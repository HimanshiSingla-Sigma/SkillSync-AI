from typing import Dict, List


class FAQService:
    """Instant offline FAQ guidance for campus recruitment queries."""

    STATIC_FAQS: List[Dict[str, str]] = [
        {
            "question": "How is my eligibility calculated?",
            "answer": "Eligibility is computed deterministically using rules set by recruiters, including CGPA thresholds, maximum allowed backlogs, eligible degree programmes, and graduation batches. The AI never guesses eligibility.",
        },
        {
            "question": "What is the difference between eligibility and match percentage?",
            "answer": "Eligibility is a binary gate (pass/fail) determining whether you can submit an application. Match percentage reflects how closely your resume skills overlap with the target job description.",
        },
        {
            "question": "How do I update missing skills extracted from my resume?",
            "answer": "You can review and edit your extracted skills in the Profile / Resume section. Any edits automatically synchronize with the AI Knowledge Graph and update your match scores.",
        },
    ]

    @classmethod
    def get_faqs(cls) -> List[Dict[str, str]]:
        return cls.STATIC_FAQS