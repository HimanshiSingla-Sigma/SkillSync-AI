from typing import Optional
from app.sync.student_sync import StudentSync
from app.sync.company_sync import CompanySync
from app.sync.drive_sync import DriveSync
from app.sync.application_sync import ApplicationSync


class SyncManager:
    """Central registry and dispatch manager for graph synchronizers."""

    def __init__(
        self,
        student_sync: Optional[StudentSync] = None,
        company_sync: Optional[CompanySync] = None,
        drive_sync: Optional[DriveSync] = None,
        application_sync: Optional[ApplicationSync] = None,
    ):
        self.students = student_sync or StudentSync()
        self.companies = company_sync or CompanySync()
        self.drives = drive_sync or DriveSync()
        self.applications = application_sync or ApplicationSync()


# Global reusable singleton instance
sync_manager = SyncManager()