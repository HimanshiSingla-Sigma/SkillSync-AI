from typing import Any, Dict, List, Optional
from app.repositories.student_repository import StudentRepository
from app.sync.graph_sync_service import GraphSyncService, graph_sync_service
from app.models.student import StudentModel, StudentProfile
from app.schemas.student_schema import (
    StudentRegisterRequest,
    StudentUpdateRequest,
    StudentResponse,
    StudentProfileResponse,
)
from app.core.security import get_password_hash, verify_password, create_access_token
from app.services.skill_extraction_service import SkillExtractionService
from app.services.otp_service import OTPService
from app.utils.exceptions import BadRequestException, ConflictException, NotFoundException, UnauthorizedException


class StudentService:
    """Manages student authentication, profile updates, and graph synchronization."""

    def __init__(
        self,
        student_repo: Optional[StudentRepository] = None,
        sync_service: Optional[GraphSyncService] = None,
    ):
        self.repo = student_repo or StudentRepository()
        self.sync = sync_service or graph_sync_service

    def _to_response_dto(self, student: StudentModel) -> StudentResponse:
        return StudentResponse(
            id=str(student.id),
            email=student.email,
            full_name=student.full_name,
            role=student.role,
            is_active=student.is_active,
            profile=StudentProfileResponse(**student.profile.model_dump()),
            skills=student.skills,
            resume_id=student.resume_id,
            created_at=student.created_at,
            updated_at=student.updated_at,
        )

    async def register(self, req: StudentRegisterRequest) -> Dict[str, Any]:
        existing = await self.repo.find_by_email(req.email)
        if existing:
            raise ConflictException(f"Account with email '{req.email}' already exists.")

        # Enforce Email Verification OTP
        if req.otp:
            await OTPService.verify_otp(req.email, req.otp)
        else:
            is_verified = await OTPService.is_verified(req.email)
            if not is_verified:
                raise BadRequestException("Email verification required. Please verify your email with OTP before registering.")

        normalized_skills = SkillExtractionService.extract_and_normalize(req.skills)

        student_doc = StudentModel(
            email=req.email.lower().strip(),
            hashed_password=get_password_hash(req.password),
            full_name=req.full_name.strip(),
            role="STUDENT",
            profile=StudentProfile(
                cgpa=req.cgpa,
                backlogs=req.backlogs,
                programme=req.programme,
                branch=req.branch,
                graduation_year=req.graduation_year,
            ),
            skills=normalized_skills,
        )

        created_student = await self.repo.create(student_doc)

        # Sync with Neo4j Knowledge Graph
        await self.sync.sync_student(created_student)

        token = create_access_token(
            subject=str(created_student.id),
            role=created_student.role,
            email=created_student.email,
        )

        return {
            "access_token": token,
            "token_type": "bearer",
            "student": self._to_response_dto(created_student),
        }

    async def authenticate(self, email: str, password: str) -> Dict[str, Any]:
        student = await self.repo.find_by_email(email)
        if not student or not verify_password(password, student.hashed_password):
            raise UnauthorizedException("Invalid student email or password.")
        if not student.is_active:
            raise BadRequestException("Student account is inactive.")

        token = create_access_token(
            subject=str(student.id),
            role=student.role,
            email=student.email,
        )

        return {
            "access_token": token,
            "token_type": "bearer",
            "student": self._to_response_dto(student),
        }

    async def get_by_id(self, student_id: str) -> StudentResponse:
        student = await self.repo.find_by_id(student_id)
        if not student:
            raise NotFoundException(f"Student with ID '{student_id}' not found.")
        return self._to_response_dto(student)

    async def update_profile(self, student_id: str, req: StudentUpdateRequest) -> StudentResponse:
        student = await self.repo.find_by_id(student_id)
        if not student:
            raise NotFoundException(f"Student with ID '{student_id}' not found.")

        update_payload: Dict[str, Any] = {}
        if req.full_name is not None:
            update_payload["full_name"] = req.full_name.strip()

        current_profile = (
            student.profile.model_dump()
            if student.profile
            else {
                "cgpa": 0.0,
                "backlogs": 0,
                "programme": "B.Tech",
                "branch": "Computer Science",
                "graduation_year": 2025,
            }
        )

        if req.profile is not None:
            incoming = req.profile.model_dump(exclude_unset=True)
            current_profile.update(incoming)

        if req.cgpa is not None:
            current_profile["cgpa"] = float(req.cgpa)
        if req.backlogs is not None:
            current_profile["backlogs"] = int(req.backlogs)
        if req.programme is not None:
            current_profile["programme"] = req.programme.strip()
        if req.branch is not None:
            current_profile["branch"] = req.branch.strip()
        if req.graduation_year is not None:
            current_profile["graduation_year"] = int(req.graduation_year)

        update_payload["profile"] = current_profile

        if req.skills is not None:
            update_payload["skills"] = SkillExtractionService.extract_and_normalize(req.skills)

        updated_student = await self.repo.update(student_id, update_payload)

        # Sync update with Neo4j Knowledge Graph
        try:
            await self.sync.sync_student(updated_student)
        except Exception as e:
            logger.warning(f"Neo4j student sync warning: {e}")

        return self._to_response_dto(updated_student)

    async def update_skills(self, student_id: str, skills: List[str]) -> StudentResponse:
        student = await self.repo.find_by_id(student_id)
        if not student:
            raise NotFoundException(f"Student with ID '{student_id}' not found.")

        normalized = SkillExtractionService.extract_and_normalize(skills)
        updated_student = await self.repo.update_skills(student_id, normalized)

        # Sync skills with Neo4j Knowledge Graph
        await self.sync.sync_student(updated_student)

        return self._to_response_dto(updated_student)

    async def list_students(self, skip: int = 0, limit: int = 100) -> List[StudentResponse]:
        students = await self.repo.list_all(skip=skip, limit=limit)
        return [self._to_response_dto(s) for s in students]