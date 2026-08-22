from typing import Optional
from app.graph.application_graph import ApplicationGraphRepository
from app.models.application import ApplicationModel
from app.core.logging import logger


class ApplicationSync:
    """Synchronizes MongoDB Application events into the Neo4j graph."""

    def __init__(self, graph_repo: Optional[ApplicationGraphRepository] = None):
        self.graph_repo = graph_repo or ApplicationGraphRepository()

    async def sync(self, application: ApplicationModel) -> None:
        if not application.id:
            logger.warning("Skipping Application sync: Missing application ID.")
            return

        try:
            await self.graph_repo.upsert_application(
                application_id=str(application.id),
                student_id=str(application.student_id),
                drive_id=str(application.drive_id),
                status=application.status,
                match_percentage=application.match_percentage,
            )
            logger.info(f"Synchronized application ID '{application.id}' to Neo4j graph.")
        except Exception as e:
            logger.error(f"Failed to sync Application {application.id} to Neo4j: {str(e)}")
            raise e

    async def update_status(self, application_id: str, status: str) -> None:
        try:
            await self.graph_repo.update_application_status(str(application_id), status)
            logger.info(f"Updated status of application '{application_id}' in Neo4j to '{status}'.")
        except Exception as e:
            logger.error(f"Failed to update Application {application_id} status in Neo4j: {str(e)}")
            raise e

    async def delete(self, application_id: str) -> None:
        try:
            await self.graph_repo.delete_application_relationship(str(application_id))
            logger.info(f"Deleted application ID '{application_id}' relationship from Neo4j.")
        except Exception as e:
            logger.error(f"Failed to delete Application {application_id} from Neo4j: {str(e)}")
            raise e