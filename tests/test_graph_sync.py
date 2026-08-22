"""Tests for graph synchronization layer and parameter construction."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from app.sync.student_sync import StudentSync
from app.sync.drive_sync import DriveSync
from app.models.student import StudentModel, StudentProfile
from app.models.placement_drive import PlacementDriveModel, DriveEligibilityCriteria


@pytest.mark.asyncio
async def test_student_graph_sync_execution():
    mock_graph_repo = MagicMock()
    mock_graph_repo.upsert_student = AsyncMock(return_value={"id": "std_123"})
    mock_graph_repo.sync_student_skills = AsyncMock()

    sync = StudentSync(graph_repo=mock_graph_repo)

    student = StudentModel(
        _id="std_123",
        email="sam@university.edu",
        hashed_password="hash",
        full_name="Sam Smith",
        skills=["python", "fastapi", "neo4j"],
        profile=StudentProfile(
            cgpa=9.1,
            backlogs=0,
            graduation_year=2025,
            programme="B.Tech Computer Science",
            branch="Computer Science",
        ),
    )

    await sync.sync(student)

    mock_graph_repo.upsert_student.assert_called_once_with(
        student_id="std_123",
        email="sam@university.edu",
        full_name="Sam Smith",
        cgpa=9.1,
        backlogs=0,
        graduation_year=2025,
        programme="B.Tech Computer Science",
        branch="Computer Science",
    )
    mock_graph_repo.sync_student_skills.assert_called_once_with(
        student_id="std_123",
        skill_names=["python", "fastapi", "neo4j"],
    )


@pytest.mark.asyncio
async def test_drive_graph_sync_execution():
    mock_graph_repo = MagicMock()
    mock_graph_repo.upsert_drive = AsyncMock(return_value={"id": "drv_456"})

    sync = DriveSync(graph_repo=mock_graph_repo)

    drive = PlacementDriveModel(
        _id="drv_456",
        company_id="cmp_789",
        company_name="HyperScale",
        title="AI Engineer",
        role_type="Full-Time",
        salary_package="20 LPA",
        job_description="AI/ML developer",
        required_skills=["python", "pytorch"],
        eligibility_criteria=DriveEligibilityCriteria(
            min_cgpa=8.0,
            max_backlogs=0,
            allowed_programmes=["B.Tech Computer Science"],
            mandatory_skills=["python"],
        ),
    )

    await sync.sync(drive)

    mock_graph_repo.upsert_drive.assert_called_once()