"""Unit tests for deterministic eligibility policies and composite evaluation."""

import pytest
from app.models.student import StudentModel, StudentProfile
from app.models.placement_drive import PlacementDriveModel, DriveEligibilityCriteria
from app.eligibility.cgpa_policy import CGPAPolicy
from app.eligibility.backlog_policy import BacklogPolicy
from app.eligibility.graduation_year_policy import GraduationYearPolicy
from app.eligibility.programme_policy import ProgrammePolicy
from app.eligibility.skill_policy import SkillPolicy
from app.eligibility.composite_eligibility_policy import CompositeEligibilityPolicy


@pytest.fixture
def sample_student():
    return StudentModel(
        _id="507f1f77bcf86cd799439011",
        email="test.student@example.com",
        hashed_password="hash",
        full_name="Alex Turner",
        skills=["python", "fastapi", "sql", "docker"],
        profile=StudentProfile(
            cgpa=8.5,
            backlogs=0,
            programme="B.Tech Computer Science",
            branch="Computer Science",
            graduation_year=2025,
        ),
    )


@pytest.fixture
def sample_drive():
    return PlacementDriveModel(
        _id="507f1f77bcf86cd799439022",
        company_id="507f1f77bcf86cd799439033",
        company_name="TechCorp",
        title="Backend Software Engineer",
        salary_package="12 LPA",
        job_description="Seeking a strong Python Backend Developer.",
        required_skills=["python", "fastapi", "docker", "aws"],
        eligibility_criteria=DriveEligibilityCriteria(
            min_cgpa=7.0,
            max_backlogs=0,
            allowed_programmes=["B.Tech Computer Science", "B.Tech IT"],
            allowed_graduation_years=[2025],
            mandatory_skills=["python", "fastapi"],
        ),
    )


def test_cgpa_policy_pass_and_fail(sample_student, sample_drive):
    policy = CGPAPolicy()
    
    # Passing test
    result = policy.evaluate(sample_student, sample_drive)
    assert result.passed is True
    assert result.status == "PASS"

    # Failing test
    sample_student.profile.cgpa = 6.5
    fail_result = policy.evaluate(sample_student, sample_drive)
    assert fail_result.passed is False
    assert fail_result.status == "FAIL"


def test_backlog_policy_pass_and_fail(sample_student, sample_drive):
    policy = BacklogPolicy()
    
    # 0 backlogs allowed, student has 0
    assert policy.evaluate(sample_student, sample_drive).passed is True

    # Student has 1 backlog
    sample_student.profile.backlogs = 1
    assert policy.evaluate(sample_student, sample_drive).passed is False


def test_graduation_year_policy(sample_student, sample_drive):
    policy = GraduationYearPolicy()
    assert policy.evaluate(sample_student, sample_drive).passed is True

    sample_student.profile.graduation_year = 2026
    assert policy.evaluate(sample_student, sample_drive).passed is False


def test_programme_policy(sample_student, sample_drive):
    policy = ProgrammePolicy()
    assert policy.evaluate(sample_student, sample_drive).passed is True

    sample_student.profile.programme = "Mechanical Engineering"
    sample_student.profile.branch = "Mechanical"
    assert policy.evaluate(sample_student, sample_drive).passed is False


def test_skill_policy_mandatory_verification(sample_student, sample_drive):
    policy = SkillPolicy()
    # Student has ["python", "fastapi"] -> PASS
    assert policy.evaluate(sample_student, sample_drive).passed is True

    # Remove required mandatory skill
    sample_student.skills = ["sql", "docker"]
    eval_fail = policy.evaluate(sample_student, sample_drive)
    assert eval_fail.passed is False
    assert "missing mandatory required skills" in eval_fail.message.lower()


def test_composite_eligibility_engine(sample_student, sample_drive):
    composite = CompositeEligibilityPolicy()
    
    # All criteria pass
    result = composite.evaluate(sample_student, sample_drive)
    assert result.eligible is True
    assert len(result.failed_criteria) == 0

    # Fail one criterion (Backlog)
    sample_student.profile.backlogs = 2
    fail_res = composite.evaluate(sample_student, sample_drive)
    assert fail_res.eligible is False
    assert "backlogs" in fail_res.failed_criteria