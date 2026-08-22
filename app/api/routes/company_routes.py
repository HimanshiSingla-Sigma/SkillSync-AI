from typing import List
from fastapi import APIRouter, Depends, status
from app.api.dependencies import (
    get_current_user_id,
    require_admin,
    require_recruiter,
)
from app.schemas.company_schema import (
    CompanyAuthResponse,
    CompanyLoginRequest,
    CompanyRegisterRequest,
    CompanyResponse,
    CompanyUpdateRequest,
)
from app.services.company_service import CompanyService
from app.utils.validators import validate_object_id

router = APIRouter(prefix="/companies", tags=["Companies"])
company_service = CompanyService()


@router.post(
    "/register",
    response_model=CompanyAuthResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_company(req: CompanyRegisterRequest):
    """Registers a new company/recruiter entity and creates Neo4j Company node."""
    return await company_service.register(req)


@router.post("/login", response_model=CompanyAuthResponse)
async def login_company(req: CompanyLoginRequest):
    """Authenticates company/recruiter and generates JWT access token."""
    return await company_service.authenticate(req.email, req.password)


@router.get(
    "/profile/me",
    response_model=CompanyResponse,
    dependencies=[Depends(require_recruiter)],
)
async def get_my_company_profile(company_id: str = Depends(get_current_user_id)):
    """Retrieves current logged-in recruiter company profile."""
    return await company_service.get_by_id(company_id)


@router.put(
    "/profile/me",
    response_model=CompanyResponse,
    dependencies=[Depends(require_recruiter)],
)
async def update_my_company_profile(
    req: CompanyUpdateRequest, company_id: str = Depends(get_current_user_id)
):
    """Updates company profile and synchronizes with Neo4j."""
    return await company_service.update(company_id, req)


@router.get("/public", response_model=List[CompanyResponse])
async def list_all_companies(skip: int = 0, limit: int = 100):
    """Public catalog of all recruiting partner companies."""
    return await company_service.list_all(skip=skip, limit=limit)


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company_by_id(company_id: str):
    """Retrieves public details of a specific company."""
    validate_object_id(company_id, "Company")
    return await company_service.get_by_id(company_id)