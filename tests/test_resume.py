"""Tests for resume information extraction and canonical skill mapping."""

from app.services.skill_extraction_service import SkillExtractionService
from app.resume_processing.skill_extractor import ResumeSkillExtractor
from app.resume_processing.information_extractor import InformationExtractor


def test_lexicon_skill_normalization():
    assert SkillExtractionService.normalize_skill("python3") == "python"
    assert SkillExtractionService.normalize_skill("react.js") == "react"
    assert SkillExtractionService.normalize_skill("k8s") == "kubernetes"
    assert SkillExtractionService.normalize_skill("postgres") == "postgresql"
    assert SkillExtractionService.normalize_skill("drf") == "django"


def test_resume_text_skill_extraction():
    sample_text = """
    EXPERIENCE SUMMARY:
    Experienced in developing microservices using FastAPI, Docker, and MongoDB.
    Familiar with AWS EC2 deployment, CI/CD pipelines with Git, and Cypher queries in Neo4j.
    """
    extracted = ResumeSkillExtractor.extract_skills_from_text(sample_text)

    expected = {"fastapi", "docker", "mongodb", "aws", "ci/cd", "git", "neo4j"}
    assert expected.issubset(set(extracted))


def test_regex_structured_information_extraction():
    sample_cv = """
    Rahul Sharma
    rahul.sharma2025@gmail.com
    +91 9876543210
    
    EDUCATION:
    B.Tech Computer Science and Engineering
    CGPA: 8.92 / 10
    Batch: 2025
    """
    data = InformationExtractor.extract_structured_sections(sample_cv)

    assert data["name"] == "Rahul Sharma"
    assert data["email"] == "rahul.sharma2025@gmail.com"
    assert data["phone"] == "919876543210"
    assert len(data["education"]) > 0
    assert data["education"][0].degree == "B.Tech"
    assert data["education"][0].branch == "Computer Science"
    assert data["education"][0].cgpa == 8.92
    assert data["education"][0].graduation_year == 2025