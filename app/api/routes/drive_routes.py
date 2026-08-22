from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Query, status
from app.api.dependencies import (
    get_current_user_id,
    get_current_user_token_payload,
    require_recruiter,
)
from app.schemas.drive_schema import (
    DriveCreateRequest,
    DriveResponse,
    DriveUpdateRequest,
)
from app.services.drive_service import DriveService
from app.utils.validators import validate_object_id

router = APIRouter(prefix="/drives", tags=["Placement Drives"])
drive_service = DriveService()


@router.post(
    "/",
    response_model=DriveResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_recruiter)],
)
async def create_placement_drive(
    req: DriveCreateRequest, company_id: str = Depends(get_current_user_id)
):
    """Creates a new placement drive, saves deterministic criteria, and establishes Neo4j graph edges."""
    return await drive_service.create_drive(company_id, req)


@router.get("/", response_model=List[DriveResponse])
async def list_published_drives(
    status_filter: Optional[str] = Query("PUBLISHED", alias="status"),
    skip: int = 0,
    limit: int = 100,
):
    """Lists published placement drives open for candidate discovery."""
    return await drive_service.list_drives(
        status=status_filter, skip=skip, limit=limit
    )


@router.get(
    "/company/my-drives",
    response_model=List[DriveResponse],
    dependencies=[Depends(require_recruiter)],
)
async def list_my_company_drives(
    company_id: str = Depends(get_current_user_id),
):
    """Lists all recruitment drives posted by the logged-in recruiter."""
    return await drive_service.list_by_company(company_id)


@router.get("/{drive_id}", response_model=DriveResponse)
async def get_drive_details(drive_id: str):
    """Retrieves full details and criteria for a specific placement drive."""
    validate_object_id(drive_id, "Placement Drive")
    return await drive_service.get_by_id(drive_id)


@router.put(
    "/{drive_id}",
    response_model=DriveResponse,
    dependencies=[Depends(require_recruiter)],
)
async def update_placement_drive(
    drive_id: str,
    req: DriveUpdateRequest,
    token_payload: Dict[str, Any] = Depends(get_current_user_token_payload),
):
    """Updates job description, packages, criteria, or status, synchronizing with Neo4j."""
    validate_object_id(drive_id, "Placement Drive")
    user_id = token_payload["sub"]
    role = token_payload["role"]
    return await drive_service.update_drive(drive_id, user_id, req, role)