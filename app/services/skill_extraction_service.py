import re
from typing import List, Set


class SkillExtractionService:
    """
    Deterministic lexicon-based skill identifier and normalizer.
    Transforms diverse candidate keywords into uniform lowercase tokens.
    """

    CANONICAL_SKILL_LEXICON = {
        # Programming & Frameworks
        "python": ["python", "python3", "py", "python scripting"],
        "java": ["java", "core java", "java 8", "java 11", "java 17"],
        "c++": ["c++", "cpp"],
        "c": ["c lang", "c programming"],
        "c#": ["c#", "csharp", "c sharp"],
        "javascript": ["javascript", "js", "ecmascript"],
        "typescript": ["typescript", "ts"],
        "go": ["golang", "go programming"],
        "rust": ["rust", "rustlang"],
        "sql": ["sql", "structured query language", "pl/sql", "tsql"],
        "html": ["html", "html5"],
        "css": ["css", "css3"],
        "react": ["react", "react.js", "reactjs"],
        "node.js": ["node", "nodejs", "node.js"],
        "fastapi": ["fastapi", "fast-api"],
        "django": ["django", "django rest framework", "drf"],
        "flask": ["flask"],
        "spring boot": ["spring boot", "springboot", "spring framework"],
        "angular": ["angular", "angularjs"],
        "vue": ["vue", "vue.js", "vuejs"],

        # Databases & Big Data
        "mongodb": ["mongodb", "mongo", "nosql mongodb"],
        "postgresql": ["postgres", "postgresql", "pg"],
        "mysql": ["mysql"],
        "redis": ["redis"],
        "neo4j": ["neo4j", "graph database", "cypher"],
        "elasticsearch": ["elasticsearch", "elastic search", "elk"],
        "kafka": ["apache kafka", "kafka"],

        # Cloud, DevOps & Tools
        "aws": ["aws", "amazon web services", "ec2", "s3", "lambda"],
        "azure": ["azure", "microsoft azure"],
        "gcp": ["gcp", "google cloud", "google cloud platform"],
        "docker": ["docker", "containerization", "containers"],
        "kubernetes": ["kubernetes", "k8s"],
        "git": ["git", "github", "gitlab"],
        "linux": ["linux", "ubuntu", "unix", "bash", "shell scripting"],
        "ci/cd": ["ci/cd", "continuous integration", "jenkins", "github actions"],

        # AI/ML & Data Science
        "machine learning": ["machine learning", "ml", "supervised learning"],
        "deep learning": ["deep learning", "neural networks"],
        "nlp": ["nlp", "natural language processing"],
        "rag": ["rag", "graphrag", "retrieval augmented generation"],
        "langchain": ["langchain"],
        "pytorch": ["pytorch"],
        "tensorflow": ["tensorflow", "keras"],
        "pandas": ["pandas"],
        "numpy": ["numpy"],
        "scikit-learn": ["scikit-learn", "sklearn"],
    }

    @classmethod
    def normalize_skill(cls, raw_skill: str) -> str:
        """Converts raw string variations into canonical standard skill identifiers."""
        clean = raw_skill.strip().lower()
        for canonical, aliases in cls.CANONICAL_SKILL_LEXICON.items():
            if clean == canonical or clean in aliases:
                return canonical
        return clean

    @classmethod
    def extract_and_normalize(cls, raw_skills: List[str]) -> List[str]:
        """Deduplicates and canonicalizes a collection of skill inputs."""
        normalized: Set[str] = set()
        for s in raw_skills:
            if s and s.strip():
                normalized.add(cls.normalize_skill(s))
        return sorted(list(normalized))

    @classmethod
    def extract_from_text(cls, text: str) -> List[str]:
        """Scans arbitrary plain text against known technical aliases using boundary regex."""
        found_skills: Set[str] = set()
        lowered_text = f" {text.lower()} "

        for canonical, aliases in cls.CANONICAL_SKILL_LEXICON.items():
            for alias in aliases:
                escaped = re.escape(alias)
                pattern = rf"(?:\b|\s){escaped}(?:\b|\s)"
                if re.search(pattern, lowered_text):
                    found_skills.add(canonical)
                    break

        return sorted(list(found_skills))