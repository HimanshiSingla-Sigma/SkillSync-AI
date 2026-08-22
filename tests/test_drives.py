"""Tests for placement drive publishing, skill normalization, and retrieval."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.drive_service import DriveService
from app.models.company import CompanyModel
from app.models.placement_drive import PlacementDriveModel, DriveEligibilityCriteria
from app.schemas.drive_schema import DriveCreateRequest, DriveEligibilityCriteriaSchema


@pytest.mark.asyncio
async def test_drive_creation_and_skill_normalization():
    mock_drive_repo = MagicMock()
    mock_company_repo = MagicMock()
    mock_sync = MagicMock()
    mock_sync.sync_drive = AsyncMock()

    company_doc = CompanyModel(
        _id="65f011112222333344445555",
        name="Alpha Dynamics",
        email="talent@alphadynamics.com",
        hashed_password="hash",
    )
    mock_company_repo.find_by_id = AsyncMock(return_value=company_doc)

    created_drive = PlacementDriveModel(
        _id="65f088889999000011112222",
        company_id=str(company_doc.id),
        company_name="Alpha Dynamics",
        title="Full Stack Software Engineer",
        salary_package="15 LPA",
        job_description="Seeking engineers skilled in Node, React, and AWS.",
        required_skills=["node.js", "react", "aws"],
        eligibility_criteria=DriveEligibilityCriteria(
            min_cgpa=8.0,
            max_backlogs=0,
            mandatory_skills=["react"],
        ),
    )
    mock_drive_repo.create = AsyncMock(return_value=created_drive)

    service = DriveService(
        drive_repo=mock_drive_repo,
        company_repo=mock_company_repo,
        sync_service=mock_sync,
    )

    req = DriveCreateRequest(
        title="Full Stack Software Engineer",
        salary_package="15 LPA",
        job_description="Seeking engineers skilled in Node, React, and AWS.",
        required_skills=["NodeJS", "React.js", "AWS"],
        eligibility_criteria=DriveEligibilityCriteriaSchema(
            min_cgpa=8.0,
            max_backlogs=0,
            mandatory_skills=["React"],
        ),
    )

    res = await service.create_drive(str(company_doc.id), req)

    assert res.title == "Full Stack Software Engineer"
    assert "node.js" in res.required_skills
    assert "react" in res.required_skills
    mock_sync.sync_drive.assert_called_once()