from typing import Optional
from app.sync.sync_manager import SyncManager, sync_manager
from app.models.student import StudentModel
from app.models.company import CompanyModel
from app.models.placement_drive import PlacementDriveModel
from app.models.application import ApplicationModel
from app.core.logging import logger


class GraphSyncService:
    """
    Orchestration service called by business layers after successful MongoDB operations.
    Ensures MongoDB remains the authoritative source of truth while keeping Neo4j in sync.
    """

    def __init__(self, manager: Optional[SyncManager] = None):
        self.manager = manager or sync_manager

    async def sync_student(self, student: StudentModel) -> None:
        await self.manager.students.sync(student)

    async def delete_student(self, student_id: str) -> None:
        await self.manager.students.delete(student_id)

    async def sync_company(self, company: CompanyModel) -> None:
        await self.manager.companies.sync(company)

    async def delete_company(self, company_id: str) -> None:
        await self.manager.companies.delete(company_id)

    async def sync_drive(self, drive: PlacementDriveModel) -> None:
        await self.manager.drives.sync(drive)

    async def delete_drive(self, drive_id: str) -> None:
        await self.manager.drives.delete(drive_id)

    async def sync_application(self, application: ApplicationModel) -> None:
        await self.manager.applications.sync(application)

    async def update_application_status(self, application_id: str, status: str) -> None:
        await self.manager.applications.update_status(application_id, status)

    async def delete_application(self, application_id: str) -> None:
        await self.manager.applications.delete(application_id)


# Global singleton instance
graph_sync_service = GraphSyncService()