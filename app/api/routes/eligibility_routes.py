from fastapi import APIRouter, Depends
from app.api.dependencies import get_current_user_id, require_student
from app.schemas.eligibility_schema import EligibilityCheckResponse
from app.services.eligibility_service import EligibilityService
from app.utils.validators import validate_object_id

router = APIRouter(prefix="/eligibility", tags=["Eligibility & Matching"])
eligibility_service = EligibilityService()


@router.get(
    "/check/{drive_id}",
    response_model=EligibilityCheckResponse,
    dependencies=[Depends(require_student)],
)
async def check_drive_eligibility(
    drive_id: str, student_id: str = Depends(get_current_user_id)
):
    """
    Executes deterministic composite policy evaluation:
    - CGPA Check
    - Backlog Check
    - Programme / Branch Check
    - Graduation Year Check
    - Mandatory Skill Policy Check
    - Overlap & Missing Skill Match Percentage Calculation
    """
    validate_object_id(drive_id, "Placement Drive")
    return await eligibility_service.check_eligibility(student_id, drive_id)