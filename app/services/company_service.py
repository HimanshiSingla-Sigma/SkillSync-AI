from typing import Any, Dict, List, Optional
from app.repositories.company_repository import CompanyRepository
from app.sync.graph_sync_service import GraphSyncService, graph_sync_service
from app.models.company import CompanyModel
from app.schemas.company_schema import (
    CompanyRegisterRequest,
    CompanyUpdateRequest,
    CompanyResponse,
)
from app.core.security import get_password_hash, verify_password, create_access_token
from app.services.otp_service import OTPService
from app.utils.exceptions import BadRequestException, ConflictException, NotFoundException, UnauthorizedException


class CompanyService:
    """Manages company/recruiter accounts, profiles, and graph synchronizations."""

    def __init__(
        self,
        company_repo: Optional[CompanyRepository] = None,
        sync_service: Optional[GraphSyncService] = None,
    ):
        self.repo = company_repo or CompanyRepository()
        self.sync = sync_service or graph_sync_service

    def _to_response_dto(self, company: CompanyModel) -> CompanyResponse:
        return CompanyResponse(
            id=str(company.id),
            name=company.name,
            email=company.email,
            role=company.role,
            is_active=company.is_active,
            industry=company.industry,
            website=company.website,
            description=company.description,
            location=company.location,
            created_at=company.created_at,
            updated_at=company.updated_at,
        )

    async def register(self, req: CompanyRegisterRequest) -> Dict[str, Any]:
        existing = await self.repo.find_by_email(req.email)
        if existing:
            raise ConflictException(f"Company account with email '{req.email}' already exists.")

        # Enforce Email Verification OTP
        if req.otp:
            await OTPService.verify_otp(req.email, req.otp)
        else:
            is_verified = await OTPService.is_verified(req.email)
            if not is_verified:
                raise BadRequestException("Email verification required. Please verify your recruiter email with OTP before registering.")

        company_doc = CompanyModel(
            name=req.name.strip(),
            email=req.email.lower().strip(),
            hashed_password=get_password_hash(req.password),
            role="RECRUITER",
            industry=req.industry.strip(),
            website=req.website,
            description=req.description,
            location=req.location,
        )

        created_company = await self.repo.create(company_doc)

        # Sync with Neo4j Knowledge Graph
        await self.sync.sync_company(created_company)

        token = create_access_token(
            subject=str(created_company.id),
            role=created_company.role,
            email=created_company.email,
        )

        return {
            "access_token": token,
            "token_type": "bearer",
            "company": self._to_response_dto(created_company),
        }

    async def authenticate(self, email: str, password: str) -> Dict[str, Any]:
        company = await self.repo.find_by_email(email)
        if not company or not verify_password(password, company.hashed_password):
            raise UnauthorizedException("Invalid company credentials.")
        if not company.is_active:
            raise BadRequestException("Company account is inactive.")

        token = create_access_token(
            subject=str(company.id),
            role=company.role,
            email=company.email,
        )

        return {
            "access_token": token,
            "token_type": "bearer",
            "company": self._to_response_dto(company),
        }

    async def get_by_id(self, company_id: str) -> CompanyResponse:
        company = await self.repo.find_by_id(company_id)
        if not company:
            raise NotFoundException(f"Company with ID '{company_id}' not found.")
        return self._to_response_dto(company)

    async def update(self, company_id: str, req: CompanyUpdateRequest) -> CompanyResponse:
        company = await self.repo.find_by_id(company_id)
        if not company:
            raise NotFoundException(f"Company with ID '{company_id}' not found.")

        update_payload = req.model_dump(exclude_unset=True)
        updated_company = await self.repo.update(company_id, update_payload)

        # Sync with Neo4j Knowledge Graph
        await self.sync.sync_company(updated_company)

        return self._to_response_dto(updated_company)

    async def list_all(self, skip: int = 0, limit: int = 100) -> List[CompanyResponse]:
        companies = await self.repo.list_all(skip=skip, limit=limit)
        return [self._to_response_dto(c) for c in companies]