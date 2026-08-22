from typing import Any, Dict, List, Optional
from app.repositories.drive_repository import DriveRepository
from app.repositories.company_repository import CompanyRepository
from app.sync.graph_sync_service import GraphSyncService, graph_sync_service
from app.models.placement_drive import PlacementDriveModel, DriveEligibilityCriteria
from app.schemas.drive_schema import (
    DriveCreateRequest,
    DriveUpdateRequest,
    DriveResponse,
    DriveEligibilityCriteriaSchema,
)
from app.services.skill_extraction_service import SkillExtractionService
from app.services.notification_service import NotificationService
from app.utils.exceptions import ForbiddenException, NotFoundException


class DriveService:
    """Manages placement drive lifecycle, publishing rules, and graph synchronization."""

    def __init__(
        self,
        drive_repo: Optional[DriveRepository] = None,
        company_repo: Optional[CompanyRepository] = None,
        sync_service: Optional[GraphSyncService] = None,
    ):
        self.repo = drive_repo or DriveRepository()
        self.company_repo = company_repo or CompanyRepository()
        self.sync = sync_service or graph_sync_service

    def _to_response_dto(self, drive: PlacementDriveModel) -> DriveResponse:
        return DriveResponse(
            id=str(drive.id),
            company_id=drive.company_id,
            company_name=drive.company_name,
            title=drive.title,
            role_type=drive.role_type,
            salary_package=drive.salary_package,
            location=drive.location,
            job_description=drive.job_description,
            required_skills=drive.required_skills,
            eligibility_criteria=DriveEligibilityCriteriaSchema(
                **drive.eligibility_criteria.model_dump()
            ),
            status=drive.status,
            deadline=drive.deadline,
            created_at=drive.created_at,
            updated_at=drive.updated_at,
        )

    async def create_drive(self, company_id: str, req: DriveCreateRequest) -> DriveResponse:
        company = await self.company_repo.find_by_id(company_id)
        if not company:
            raise NotFoundException(f"Company with ID '{company_id}' not found.")

        normalized_required = SkillExtractionService.extract_and_normalize(req.required_skills)
        normalized_mandatory = SkillExtractionService.extract_and_normalize(
            req.eligibility_criteria.mandatory_skills
        )

        criteria_doc = DriveEligibilityCriteria(
            min_cgpa=req.eligibility_criteria.min_cgpa,
            max_backlogs=req.eligibility_criteria.max_backlogs,
            allowed_programmes=req.eligibility_criteria.allowed_programmes,
            allowed_graduation_years=req.eligibility_criteria.allowed_graduation_years,
            mandatory_skills=normalized_mandatory,
        )

        drive_doc = PlacementDriveModel(
            company_id=str(company.id),
            company_name=company.name,
            title=req.title.strip(),
            role_type=req.role_type,
            salary_package=req.salary_package.strip(),
            location=req.location,
            job_description=req.job_description,
            required_skills=normalized_required,
            eligibility_criteria=criteria_doc,
            status="PUBLISHED",
            deadline=req.deadline,
        )

        created_drive = await self.repo.create(drive_doc)

        # Sync with Neo4j Knowledge Graph
        await self.sync.sync_drive(created_drive)

        await NotificationService.notify_drive_published(
            company_name=company.name,
            drive_title=created_drive.title,
            target_programmes=created_drive.eligibility_criteria.allowed_programmes,
        )

        return self._to_response_dto(created_drive)

    async def get_by_id(self, drive_id: str) -> DriveResponse:
        drive = await self.repo.find_by_id(drive_id)
        if not drive:
            raise NotFoundException(f"Placement Drive with ID '{drive_id}' not found.")
        return self._to_response_dto(drive)

    async def list_drives(
        self,
        status: Optional[str] = "PUBLISHED",
        skip: int = 0,
        limit: int = 100,
    ) -> List[DriveResponse]:
        drives = await self.repo.list_all(status=status, skip=skip, limit=limit)
        return [self._to_response_dto(d) for d in drives]

    async def list_by_company(self, company_id: str) -> List[DriveResponse]:
        drives = await self.repo.find_by_company_id(company_id)
        return [self._to_response_dto(d) for d in drives]

    async def update_drive(
        self,
        drive_id: str,
        company_id: str,
        req: DriveUpdateRequest,
        user_role: str = "RECRUITER",
    ) -> DriveResponse:
        drive = await self.repo.find_by_id(drive_id)
        if not drive:
            raise NotFoundException(f"Placement Drive with ID '{drive_id}' not found.")

        if user_role != "ADMIN" and drive.company_id != company_id:
            raise ForbiddenException("Unauthorized to modify placement drives owned by another company.")

        update_payload: Dict[str, Any] = req.model_dump(exclude_unset=True)

        if "required_skills" in update_payload and update_payload["required_skills"]:
            update_payload["required_skills"] = SkillExtractionService.extract_and_normalize(
                update_payload["required_skills"]
            )

        if "eligibility_criteria" in update_payload and update_payload["eligibility_criteria"]:
            crit = update_payload["eligibility_criteria"]
            if "mandatory_skills" in crit:
                crit["mandatory_skills"] = SkillExtractionService.extract_and_normalize(
                    crit["mandatory_skills"]
                )
            update_payload["eligibility_criteria"] = crit

        updated_drive = await self.repo.update(drive_id, update_payload)

        # Sync with Neo4j Knowledge Graph
        await self.sync.sync_drive(updated_drive)

        return self._to_response_dto(updated_drive)