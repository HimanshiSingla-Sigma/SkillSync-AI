from typing import List, Optional
from app.repositories.application_repository import ApplicationRepository
from app.repositories.student_repository import StudentRepository
from app.repositories.drive_repository import DriveRepository
from app.repositories.company_repository import CompanyRepository
from app.sync.graph_sync_service import GraphSyncService, graph_sync_service
from app.services.eligibility_service import EligibilityService
from app.services.notification_service import NotificationService
from app.models.application import ApplicationModel, ApplicationStatus
from app.schemas.application_schema import (
    ApplicationCreateRequest,
    ApplicationResponse,
    ApplicationDetailedResponse,
    ApplicationStatusHistoryResponse,
)
from app.utils.exceptions import BadRequestException, ConflictException, ForbiddenException, NotFoundException


class ApplicationService:
    """Manages student job applications, status transitions, and application graph edges."""

    def __init__(
        self,
        app_repo: Optional[ApplicationRepository] = None,
        student_repo: Optional[StudentRepository] = None,
        drive_repo: Optional[DriveRepository] = None,
        company_repo: Optional[CompanyRepository] = None,
        eligibility_service: Optional[EligibilityService] = None,
        sync_service: Optional[GraphSyncService] = None,
    ):
        self.repo = app_repo or ApplicationRepository()
        self.student_repo = student_repo or StudentRepository()
        self.drive_repo = drive_repo or DriveRepository()
        self.company_repo = company_repo or CompanyRepository()
        self.eligibility = eligibility_service or EligibilityService()
        self.sync = sync_service or graph_sync_service

    def _to_response_dto(self, app_doc: ApplicationModel) -> ApplicationResponse:
        return ApplicationResponse(
            id=str(app_doc.id),
            student_id=app_doc.student_id,
            drive_id=app_doc.drive_id,
            company_id=app_doc.company_id,
            status=app_doc.status,
            status_history=[
                ApplicationStatusHistoryResponse(
                    status=h.status,
                    updated_by=h.updated_by,
                    remarks=h.remarks,
                    timestamp=h.timestamp,
                )
                for h in app_doc.status_history
            ],
            match_percentage=app_doc.match_percentage,
            matched_skills=app_doc.matched_skills,
            missing_skills=app_doc.missing_skills,
            eligibility_snapshot=app_doc.eligibility_snapshot,
            created_at=app_doc.created_at,
            updated_at=app_doc.updated_at,
        )

    async def apply_to_drive(self, student_id: str, req: ApplicationCreateRequest) -> ApplicationResponse:
        # Check duplicate application
        existing = await self.repo.find_by_student_and_drive(student_id, req.drive_id)
        if existing:
            raise ConflictException("You have already submitted an application to this placement drive.")

        student = await self.student_repo.find_by_id(student_id)
        if not student:
            raise NotFoundException(f"Student with ID '{student_id}' not found.")

        drive = await self.drive_repo.find_by_id(req.drive_id)
        if not drive:
            raise NotFoundException(f"Placement Drive with ID '{req.drive_id}' not found.")

        if drive.status != "PUBLISHED":
            raise BadRequestException("Applications are closed for this placement drive.")

        # 1. Deterministic Eligibility Check (Strict Gate)
        eval_result = await self.eligibility.check_eligibility(student_id, req.drive_id)
        if not eval_result.eligible:
            raise ForbiddenException(
                f"Ineligible to apply. Failed criteria: {', '.join(eval_result.failed_criteria)}. "
                f"Reasons: {' | '.join(eval_result.reasons)}"
            )

        app_doc = ApplicationModel(
            student_id=str(student.id),
            drive_id=str(drive.id),
            company_id=str(drive.company_id),
            status=ApplicationStatus.PENDING,
            match_percentage=eval_result.match_percentage,
            matched_skills=eval_result.matched_skills,
            missing_skills=eval_result.missing_skills,
            eligibility_snapshot=eval_result.model_dump(),
        )

        created_app = await self.repo.create(app_doc)

        # Sync (Student)-[:APPLIED_TO]->(PlacementDrive) with Neo4j Knowledge Graph
        await self.sync.sync_application(created_app)

        return self._to_response_dto(created_app)

    async def update_status(
        self,
        application_id: str,
        new_status: str,
        user_id: str,
        user_role: str,
        remarks: Optional[str] = None,
    ) -> ApplicationResponse:
        if new_status not in ApplicationStatus.ALL:
            raise BadRequestException(f"Invalid application status. Allowed: {ApplicationStatus.ALL}")

        app_doc = await self.repo.find_by_id(application_id)
        if not app_doc:
            raise NotFoundException(f"Application with ID '{application_id}' not found.")

        # Recruiters can only modify applications belonging to their company
        if user_role == "RECRUITER" and app_doc.company_id != user_id:
            raise ForbiddenException("Unauthorized to manage applications for another company's drive.")

        updated_app = await self.repo.update_status(
            application_id=application_id,
            new_status=new_status,
            updated_by=user_id,
            remarks=remarks,
        )

        # Sync updated status in Neo4j
        await self.sync.update_application_status(application_id, new_status)

        # Trigger notification alert
        student = await self.student_repo.find_by_id(app_doc.student_id)
        drive = await self.drive_repo.find_by_id(app_doc.drive_id)
        if student and drive:
            await NotificationService.notify_application_status_update(
                student_email=student.email,
                student_name=student.full_name,
                company_name=drive.company_name,
                drive_title=drive.title,
                new_status=new_status,
                remarks=remarks or "",
            )

        return self._to_response_dto(updated_app)

    async def get_student_applications(self, student_id: str) -> List[ApplicationDetailedResponse]:
        apps = await self.repo.find_by_student_id(student_id)
        results: List[ApplicationDetailedResponse] = []

        student = await self.student_repo.find_by_id(student_id)
        for a in apps:
            drive = await self.drive_repo.find_by_id(a.drive_id)
            results.append(
                ApplicationDetailedResponse(
                    id=str(a.id),
                    student_id=a.student_id,
                    student_name=student.full_name if student else "Unknown",
                    student_email=student.email if student else "Unknown",
                    student_cgpa=student.profile.cgpa if student else 0.0,
                    student_branch=student.profile.branch if student else "Unknown",
                    drive_id=a.drive_id,
                    drive_title=drive.title if drive else "Unknown Drive",
                    company_id=a.company_id,
                    company_name=drive.company_name if drive else "Unknown Company",
                    status=a.status,
                    status_history=[
                        ApplicationStatusHistoryResponse(
                            status=h.status,
                            updated_by=h.updated_by,
                            remarks=h.remarks,
                            timestamp=h.timestamp,
                        )
                        for h in a.status_history
                    ],
                    match_percentage=a.match_percentage,
                    matched_skills=a.matched_skills,
                    missing_skills=a.missing_skills,
                    created_at=a.created_at,
                )
            )
        return results

    async def get_drive_applicants(self, drive_id: str, company_id: str, user_role: str) -> List[ApplicationDetailedResponse]:
        drive = await self.drive_repo.find_by_id(drive_id)
        if not drive:
            raise NotFoundException(f"Placement Drive with ID '{drive_id}' not found.")

        if user_role != "ADMIN" and drive.company_id != company_id:
            raise ForbiddenException("Unauthorized to view applicants for this drive.")

        apps = await self.repo.find_by_drive_id(drive_id)
        results: List[ApplicationDetailedResponse] = []

        for a in apps:
            student = await self.student_repo.find_by_id(a.student_id)
            results.append(
                ApplicationDetailedResponse(
                    id=str(a.id),
                    student_id=a.student_id,
                    student_name=student.full_name if student else "Unknown",
                    student_email=student.email if student else "Unknown",
                    student_cgpa=student.profile.cgpa if student else 0.0,
                    student_branch=student.profile.branch if student else "Unknown",
                    drive_id=a.drive_id,
                    drive_title=drive.title,
                    company_id=drive.company_id,
                    company_name=drive.company_name,
                    status=a.status,
                    status_history=[
                        ApplicationStatusHistoryResponse(
                            status=h.status,
                            updated_by=h.updated_by,
                            remarks=h.remarks,
                            timestamp=h.timestamp,
                        )
                        for h in a.status_history
                    ],
                    match_percentage=a.match_percentage,
                    matched_skills=a.matched_skills,
                    missing_skills=a.missing_skills,
                    created_at=a.created_at,
                )
            )
        return results