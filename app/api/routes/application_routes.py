from typing import Any, Dict, List
from fastapi import APIRouter, Depends, status
from app.api.dependencies import (
    get_current_user_id,
    get_current_user_token_payload,
    require_recruiter,
    require_student,
)
from app.schemas.application_schema import (
    ApplicationCreateRequest,
    ApplicationDetailedResponse,
    ApplicationResponse,
    ApplicationStatusUpdateRequest,
)
from app.services.application_service import ApplicationService
from app.utils.validators import validate_object_id

router = APIRouter(prefix="/applications", tags=["Applications"])
application_service = ApplicationService()


@router.post(
    "/apply",
    response_model=ApplicationResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_student)],
)
async def apply_to_placement_drive(
    req: ApplicationCreateRequest,
    student_id: str = Depends(get_current_user_id),
):
    """Submits student application after strictly verifying deterministic eligibility."""
    validate_object_id(req.drive_id, "Placement Drive")
    return await application_service.apply_to_drive(student_id, req)


@router.get(
    "/student/my-applications",
    response_model=List[ApplicationDetailedResponse],
    dependencies=[Depends(require_student)],
)
async def get_my_submitted_applications(
    student_id: str = Depends(get_current_user_id),
):
    """Retrieves all placement drive applications submitted by the logged-in student."""
    return await application_service.get_student_applications(student_id)


@router.get(
    "/drive/{drive_id}/applicants",
    response_model=List[ApplicationDetailedResponse],
    dependencies=[Depends(require_recruiter)],
)
async def get_drive_applicants(
    drive_id: str,
    token_payload: Dict[str, Any] = Depends(get_current_user_token_payload),
):
    """Recruiter endpoint to view all applicants and match percentages for their drive."""
    validate_object_id(drive_id, "Placement Drive")
    company_id = token_payload["sub"]
    role = token_payload["role"]
    return await application_service.get_drive_applicants(
        drive_id, company_id, role
    )


@router.put(
    "/{application_id}/status",
    response_model=ApplicationResponse,
    dependencies=[Depends(require_recruiter)],
)
async def update_applicant_status(
    application_id: str,
    req: ApplicationStatusUpdateRequest,
    token_payload: Dict[str, Any] = Depends(get_current_user_token_payload),
):
    """Updates applicant status, stores audit history, and updates Neo4j [:APPLIED_TO] edge."""
    validate_object_id(application_id, "Application")
    user_id = token_payload["sub"]
    role = token_payload["role"]
    return await application_service.update_status(
        application_id=application_id,
        new_status=req.status,
        user_id=user_id,
        user_role=role,
        remarks=req.remarks,
    )