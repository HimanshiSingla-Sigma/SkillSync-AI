from typing import Any, Dict, List
from fastapi import APIRouter, Depends, status
from app.api.dependencies import (
    get_current_user_id,
    get_current_user_token_payload,
    require_admin,
    require_student,
)
from app.schemas.student_schema import (
    StudentAuthResponse,
    StudentLoginRequest,
    StudentRegisterRequest,
    StudentResponse,
    StudentSkillsUpdateRequest,
    StudentUpdateRequest,
)
from app.services.student_service import StudentService
from app.utils.validators import validate_object_id

router = APIRouter(prefix="/students", tags=["Students"])
student_service = StudentService()


@router.post(
    "/register",
    response_model=StudentAuthResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_student(req: StudentRegisterRequest):
    """Registers a new student account, hashes password, and creates graph node."""
    return await student_service.register(req)


@router.post("/login", response_model=StudentAuthResponse)
async def login_student(req: StudentLoginRequest):
    """Authenticates student and returns a signed JWT access token."""
    return await student_service.authenticate(req.email, req.password)


@router.get(
    "/profile/me",
    response_model=StudentResponse,
    dependencies=[Depends(require_student)],
)
async def get_my_profile(student_id: str = Depends(get_current_user_id)):
    """Retrieves the authenticated student's profile."""
    return await student_service.get_by_id(student_id)


@router.put(
    "/profile/me",
    response_model=StudentResponse,
    dependencies=[Depends(require_student)],
)
async def update_my_profile(
    req: StudentUpdateRequest, student_id: str = Depends(get_current_user_id)
):
    """Updates profile attributes (CGPA, backlogs, programme) and synchronizes with Neo4j."""
    return await student_service.update_profile(student_id, req)


@router.put(
    "/profile/me/skills",
    response_model=StudentResponse,
    dependencies=[Depends(require_student)],
)
async def update_my_skills(
    req: StudentSkillsUpdateRequest,
    student_id: str = Depends(get_current_user_id),
):
    """Updates skill set and refreshes knowledge graph (Student)-[:HAS_SKILL]->(Skill) edges."""
    return await student_service.update_skills(student_id, req.skills)


@router.get(
    "/{student_id}",
    response_model=StudentResponse,
    dependencies=[Depends(require_admin)],
)
async def get_student_by_id(student_id: str):
    """Admin endpoint to inspect any student profile."""
    validate_object_id(student_id, "Student")
    return await student_service.get_by_id(student_id)


@router.get(
    "/",
    response_model=List[StudentResponse],
    dependencies=[Depends(require_admin)],
)
async def list_all_students(skip: int = 0, limit: int = 100):
    """Admin endpoint to list all registered students."""
    return await student_service.list_students(skip=skip, limit=limit)