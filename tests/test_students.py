"""Tests for student registration, profile updates, and authentication services."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.student_service import StudentService
from app.models.student import StudentModel, StudentProfile
from app.schemas.student_schema import StudentRegisterRequest, StudentUpdateRequest
from app.utils.exceptions import ConflictException


@pytest.mark.asyncio
async def test_student_registration_success():
    mock_repo = MagicMock()
    mock_repo.find_by_email = AsyncMock(return_value=None)
    
    mock_created = StudentModel(
        _id="65f011112222333344445555",
        email="test@university.edu",
        hashed_password="hashed_pw",
        full_name="John Doe",
        skills=["python", "sql"],
        profile=StudentProfile(cgpa=8.0, programme="B.Tech Computer Science"),
    )
    mock_repo.create = AsyncMock(return_value=mock_created)
    mock_sync = MagicMock()
    mock_sync.sync_student = AsyncMock()

    service = StudentService(student_repo=mock_repo, sync_service=mock_sync)

    req = StudentRegisterRequest(
        email="test@university.edu",
        password="SecretPassword123",
        full_name="John Doe",
        cgpa=8.0,
        skills=["Python", "SQL"],
    )

    response = await service.register(req)

    assert response["student"].email == "test@university.edu"
    assert response["student"].skills == ["python", "sql"]
    assert "access_token" in response
    mock_sync.sync_student.assert_called_once()


@pytest.mark.asyncio
async def test_student_duplicate_email_conflict():
    mock_repo = MagicMock()
    mock_repo.find_by_email = AsyncMock(return_value=StudentModel(
        _id="123",
        email="duplicate@uni.edu",
        hashed_password="pw",
        full_name="Duplicate",
    ))
    mock_sync = MagicMock()

    service = StudentService(student_repo=mock_repo, sync_service=mock_sync)

    req = StudentRegisterRequest(
        email="duplicate@uni.edu",
        password="Password123",
        full_name="Duplicate User",
    )

    with pytest.raises(ConflictException):
        await service.register(req)