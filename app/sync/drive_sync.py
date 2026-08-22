from typing import Optional
from app.graph.drive_graph import DriveGraphRepository
from app.models.placement_drive import PlacementDriveModel
from app.core.logging import logger


class DriveSync:
    """Synchronizes MongoDB Placement Drive entities and criteria into Neo4j."""

    def __init__(self, graph_repo: Optional[DriveGraphRepository] = None):
        self.graph_repo = graph_repo or DriveGraphRepository()

    async def sync(self, drive: PlacementDriveModel) -> None:
        if not drive.id:
            logger.warning("Skipping Drive sync: Missing drive ID.")
            return

        try:
            # Combine general required skills and mandatory policy skills
            combined_skills = list(
                set(drive.required_skills + drive.eligibility_criteria.mandatory_skills)
            )

            await self.graph_repo.upsert_drive(
                drive_id=str(drive.id),
                company_id=str(drive.company_id),
                title=drive.title,
                role_type=drive.role_type,
                salary_package=drive.salary_package,
                status=drive.status,
                min_cgpa=drive.eligibility_criteria.min_cgpa,
                max_backlogs=drive.eligibility_criteria.max_backlogs,
                allowed_programmes=drive.eligibility_criteria.allowed_programmes,
                required_skills=combined_skills,
            )
            logger.info(f"Synchronized placement drive '{drive.title}' (ID: {drive.id}) to Neo4j graph.")
        except Exception as e:
            logger.error(f"Failed to sync PlacementDrive {drive.id} to Neo4j: {str(e)}")
            raise e

    async def delete(self, drive_id: str) -> None:
        try:
            await self.graph_repo.delete_drive_node(str(drive_id))
            logger.info(f"Deleted placement drive ID '{drive_id}' from Neo4j graph.")
        except Exception as e:
            logger.error(f"Failed to delete PlacementDrive {drive_id} from Neo4j: {str(e)}")
            raise e