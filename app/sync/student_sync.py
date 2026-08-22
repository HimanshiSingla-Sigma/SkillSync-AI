from typing import Optional
from app.graph.student_graph import StudentGraphRepository
from app.models.student import StudentModel
from app.core.logging import logger


class StudentSync:
    """Synchronizes MongoDB Student entities and skill sets into Neo4j."""

    def __init__(self, graph_repo: Optional[StudentGraphRepository] = None):
        self.graph_repo = graph_repo or StudentGraphRepository()

    async def sync(self, student: StudentModel) -> None:
        if not student.id:
            logger.warning("Skipping Student sync: Missing student ID.")
            return

        try:
            # 1. Upsert Student Node & Programme Edge
            await self.graph_repo.upsert_student(
                student_id=str(student.id),
                email=student.email,
                full_name=student.full_name,
                cgpa=student.profile.cgpa,
                backlogs=student.profile.backlogs,
                graduation_year=student.profile.graduation_year,
                programme=student.profile.programme,
                branch=student.profile.branch,
            )

            # 2. Sync (Student)-[:HAS_SKILL]->(Skill) Edges
            await self.graph_repo.sync_student_skills(
                student_id=str(student.id),
                skill_names=student.skills,
            )
            logger.info(f"Synchronized student '{student.email}' (ID: {student.id}) to Neo4j graph.")
        except Exception as e:
            logger.error(f"Failed to sync Student {student.id} to Neo4j: {str(e)}")
            raise e

    async def delete(self, student_id: str) -> None:
        try:
            await self.graph_repo.delete_student_node(str(student_id))
            logger.info(f"Deleted student ID '{student_id}' from Neo4j graph.")
        except Exception as e:
            logger.error(f"Failed to delete Student {student_id} from Neo4j: {str(e)}")
            raise e