"""Tests for student job applications and status progression."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.application_service import ApplicationService
from app.models.student import StudentModel, StudentProfile
from app.models.placement_drive import PlacementDriveModel, DriveEligibilityCriteria
from app.models.application import ApplicationModel, ApplicationStatus
from app.schemas.application_schema import ApplicationCreateRequest
from app.schemas.eligibility_schema import EligibilityCheckResponse, PolicyEvaluationDetail
from app.utils.exceptions import ForbiddenException


@pytest.mark.asyncio
async def test_apply_to_drive_success_when_eligible():
    mock_app_repo = MagicMock()
    mock_app_repo.find_by_student_and_drive = AsyncMock(return_value=None)
    
    mock_student_repo = MagicMock()
    mock_student = StudentModel(
        _id="65f011112222333344445555",
        email="alex@uni.edu",
        hashed_password="pw",
        full_name="Alex",
        skills=["python", "fastapi"],
        profile=StudentProfile(cgpa=8.5),
    )
    mock_student_repo.find_by_id = AsyncMock(return_value=mock_student)

    mock_drive_repo = MagicMock()
    mock_drive = PlacementDriveModel(
        _id="65f022223333444455556666",
        company_id="65f033334444555566667777",
        company_name="CloudNine",
        title="Python Dev",
        salary_package="10 LPA",
        job_description="Description",
        status="PUBLISHED",
    )
    mock_drive_repo.find_by_id = AsyncMock(return_value=mock_drive)

    mock_eligibility = MagicMock()
    mock_eligibility.check_eligibility = AsyncMock(
        return_value=EligibilityCheckResponse(
            student_id="65f011112222333344445555",
            drive_id="65f022223333444455556666",
            eligible=True,
            criteria={"cgpa": "PASS", "skills": "PASS"},
            passed_criteria=["cgpa", "skills"],
            failed_criteria=[],
            reasons=[],
            policy_details={},
            match_percentage=100.0,
            matched_skills=["python", "fastapi"],
            missing_skills=[],
        )
    )

    created_app = ApplicationModel(
        _id="65f044445555666677778888",
        student_id="65f011112222333344445555",
        drive_id="65f022223333444455556666",
        company_id="65f033334444555566667777",
        status=ApplicationStatus.PENDING,
        match_percentage=100.0,
    )
    mock_app_repo.create = AsyncMock(return_value=created_app)
    mock_sync = MagicMock()
    mock_sync.sync_application = AsyncMock()

    service = ApplicationService(
        app_repo=mock_app_repo,
        student_repo=mock_student_repo,
        drive_repo=mock_drive_repo,
        eligibility_service=mock_eligibility,
        sync_service=mock_sync,
    )

    req = ApplicationCreateRequest(drive_id="65f022223333444455556666")
    res = await service.apply_to_drive("65f011112222333344445555", req)

    assert res.status == ApplicationStatus.PENDING
    assert res.match_percentage == 100.0
    mock_sync.sync_application.assert_called_once()


@pytest.mark.asyncio
async def test_apply_to_drive_rejected_when_ineligible():
    mock_app_repo = MagicMock()
    mock_app_repo.find_by_student_and_drive = AsyncMock(return_value=None)
    mock_student_repo = MagicMock()
    mock_student_repo.find_by_id = AsyncMock(return_value=StudentModel(
        _id="111", email="e@e.com", hashed_password="p", full_name="N"
    ))
    mock_drive_repo = MagicMock()
    mock_drive_repo.find_by_id = AsyncMock(return_value=PlacementDriveModel(
        _id="222", company_id="333", company_name="C", title="T", salary_package="S", job_description="JD", status="PUBLISHED"
    ))

    mock_eligibility = MagicMock()
    mock_eligibility.check_eligibility = AsyncMock(
        return_value=EligibilityCheckResponse(
            student_id="111",
            drive_id="222",
            eligible=False,
            criteria={"cgpa": "FAIL"},
            passed_criteria=[],
            failed_criteria=["cgpa"],
            reasons=["CGPA below threshold."],
            policy_details={},
            match_percentage=40.0,
            matched_skills=[],
            missing_skills=["python"],
        )
    )

    service = ApplicationService(
        app_repo=mock_app_repo,
        student_repo=mock_student_repo,
        drive_repo=mock_drive_repo,
        eligibility_service=mock_eligibility,
    )

    req = ApplicationCreateRequest(drive_id="222")

    with pytest.raises(ForbiddenException):
        await service.apply_to_drive("111", req)