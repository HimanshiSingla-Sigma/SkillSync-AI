from typing import Any, Dict, List, Optional
from app.graph.graph_repository import GraphRepository


class StudentGraphRepository(GraphRepository):
    """Manages (Student), (Programme), and [:HAS_SKILL], [:STUDIES] relationships."""

    async def upsert_student(
        self,
        student_id: str,
        email: str,
        full_name: str,
        cgpa: float,
        backlogs: int,
        graduation_year: int,
        programme: str,
        branch: str,
    ) -> Dict[str, Any]:
        """Creates or updates a Student node and links them to their academic Programme."""
        query = """
        MERGE (s:Student {id: $student_id})
        ON CREATE SET 
            s.email = $email,
            s.full_name = $full_name,
            s.cgpa = $cgpa,
            s.backlogs = $backlogs,
            s.graduation_year = $graduation_year,
            s.branch = $branch,
            s.created_at = datetime()
        ON MATCH SET 
            s.email = $email,
            s.full_name = $full_name,
            s.cgpa = $cgpa,
            s.backlogs = $backlogs,
            s.graduation_year = $graduation_year,
            s.branch = $branch,
            s.updated_at = datetime()
        
        WITH s
        WHERE $programme <> ""
        MERGE (p:Programme {name: $programme})
        MERGE (s)-[:STUDIES]->(p)
        
        RETURN s.id AS id, s.email AS email, s.full_name AS full_name
        """
        params = {
            "student_id": str(student_id),
            "email": email.strip().lower(),
            "full_name": full_name.strip(),
            "cgpa": float(cgpa),
            "backlogs": int(backlogs),
            "graduation_year": int(graduation_year),
            "programme": programme.strip(),
            "branch": branch.strip(),
        }
        res = await self.execute_write(query, params)
        return res[0] if res else {}

    async def sync_student_skills(self, student_id: str, skill_names: List[str]) -> None:
        """
        Idempotently synchronizes a student's skills.
        Removes obsolete [:HAS_SKILL] relationships and merges new active ones.
        """
        normalized_skills = [s.strip().lower() for s in skill_names if s.strip()]

        query = """
        MATCH (s:Student {id: $student_id})
        
        // 1. Remove old relationships that are no longer present
        OPTIONAL MATCH (s)-[r:HAS_SKILL]->(old_skill:Skill)
        WHERE NOT old_skill.normalized_name IN $skills
        DELETE r
        
        WITH s
        // 2. Unwind and merge each active skill
        UNWIND $skills AS skill_norm
        MERGE (sk:Skill {normalized_name: skill_norm})
        ON CREATE SET sk.name = skill_norm, sk.category = 'General', sk.created_at = datetime()
        MERGE (s)-[:HAS_SKILL]->(sk)
        """
        params = {
            "student_id": str(student_id),
            "skills": normalized_skills,
        }
        await self.execute_write(query, params)

    async def get_student_profile_graph(self, student_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves student details, enrolled programme, and all linked skills."""
        query = """
        MATCH (s:Student {id: $student_id})
        OPTIONAL MATCH (s)-[:STUDIES]->(p:Programme)
        OPTIONAL MATCH (s)-[:HAS_SKILL]->(sk:Skill)
        RETURN 
            s.id AS id,
            s.email AS email,
            s.full_name AS full_name,
            s.cgpa AS cgpa,
            s.backlogs AS backlogs,
            s.graduation_year AS graduation_year,
            s.branch AS branch,
            p.name AS programme,
            collect(DISTINCT sk.normalized_name) AS skills
        """
        res = await self.execute_read(query, {"student_id": str(student_id)})
        return res[0] if res else None

    async def delete_student_node(self, student_id: str) -> None:
        """Detaches and deletes a Student node from the graph."""
        query = """
        MATCH (s:Student {id: $student_id})
        DETACH DELETE s
        """
        await self.execute_write(query, {"student_id": str(student_id)})