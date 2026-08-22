"""Tests for company entity creation, authentication, and retrieval."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.company_service import CompanyService
from app.models.company import CompanyModel
from app.schemas.company_schema import CompanyRegisterRequest


@pytest.mark.asyncio
async def test_company_registration_and_sync():
    mock_repo = MagicMock()
    mock_repo.find_by_email = AsyncMock(return_value=None)
    
    mock_company = CompanyModel(
        _id="65f022223333444455556666",
        name="Global Cloud Systems",
        email="hr@globalcloud.com",
        hashed_password="hashed_pw",
        industry="Cloud Computing",
    )
    mock_repo.create = AsyncMock(return_value=mock_company)
    mock_sync = MagicMock()
    mock_sync.sync_company = AsyncMock()

    service = CompanyService(company_repo=mock_repo, sync_service=mock_sync)

    req = CompanyRegisterRequest(
        name="Global Cloud Systems",
        email="hr@globalcloud.com",
        password="SecureRecruiterPass1!",
        industry="Cloud Computing",
    )

    res = await service.register(req)

    assert res["company"].name == "Global Cloud Systems"
    assert res["company"].email == "hr@globalcloud.com"
    mock_sync.sync_company.assert_called_once()