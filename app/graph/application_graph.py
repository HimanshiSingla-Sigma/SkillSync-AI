from typing import Any, Dict, Optional
from app.graph.graph_repository import GraphRepository


class ApplicationGraphRepository(GraphRepository):
    """Manages (Student)-[:APPLIED_TO]->(PlacementDrive) relationships."""

    async def upsert_application(
        self,
        application_id: str,
        student_id: str,
        drive_id: str,
        status: str,
        match_percentage: float,
    ) -> Dict[str, Any]:
        """Idempotently creates or updates the APPLIED_TO edge."""
        query = """
        MATCH (s:Student {id: $student_id})
        MATCH (d:PlacementDrive {id: $drive_id})
        MERGE (s)-[r:APPLIED_TO {application_id: $application_id}]->(d)
        ON CREATE SET 
            r.status = $status,
            r.match_percentage = $match_percentage,
            r.applied_at = datetime()
        ON MATCH SET 
            r.status = $status,
            r.match_percentage = $match_percentage,
            r.updated_at = datetime()
        RETURN r.application_id AS application_id, r.status AS status, r.match_percentage AS match_percentage
        """
        params = {
            "application_id": str(application_id),
            "student_id": str(student_id),
            "drive_id": str(drive_id),
            "status": status,
            "match_percentage": float(match_percentage),
        }
        res = await self.execute_write(query, params)
        return res[0] if res else {}

    async def update_application_status(self, application_id: str, status: str) -> Optional[Dict[str, Any]]:
        """Updates the status attribute on the APPLIED_TO relationship."""
        query = """
        MATCH ()-[r:APPLIED_TO {application_id: $application_id}]->()
        SET r.status = $status, r.updated_at = datetime()
        RETURN r.application_id AS application_id, r.status AS status
        """
        res = await self.execute_write(query, {"application_id": str(application_id), "status": status})
        return res[0] if res else None

    async def delete_application_relationship(self, application_id: str) -> None:
        """Deletes the APPLIED_TO relationship."""
        query = """
        MATCH ()-[r:APPLIED_TO {application_id: $application_id}]->()
        DELETE r
        """
        await self.execute_write(query, {"application_id": str(application_id)})