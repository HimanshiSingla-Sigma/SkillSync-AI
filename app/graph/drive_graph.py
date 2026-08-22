from typing import Any, Dict, List, Optional
from app.graph.graph_repository import GraphRepository


class DriveGraphRepository(GraphRepository):
    """
    Manages (PlacementDrive) nodes and their graph edges:
    - (Company)-[:POSTS]->(PlacementDrive)
    - (PlacementDrive)-[:REQUIRES]->(Skill)
    - (PlacementDrive)-[:FOR_PROGRAMME]->(Programme)
    """

    async def upsert_drive(
        self,
        drive_id: str,
        company_id: str,
        title: str,
        role_type: str,
        salary_package: str,
        status: str,
        min_cgpa: float,
        max_backlogs: int,
        allowed_programmes: List[str],
        required_skills: List[str],
    ) -> Dict[str, Any]:
        """Creates or updates a PlacementDrive node and reconstructs its domain edges."""
        normalized_skills = [s.strip().lower() for s in required_skills if s.strip()]

        query = """
        MERGE (d:PlacementDrive {id: $drive_id})
        ON CREATE SET 
            d.title = $title,
            d.role_type = $role_type,
            d.salary_package = $salary_package,
            d.status = $status,
            d.min_cgpa = $min_cgpa,
            d.max_backlogs = $max_backlogs,
            d.created_at = datetime()
        ON MATCH SET 
            d.title = $title,
            d.role_type = $role_type,
            d.salary_package = $salary_package,
            d.status = $status,
            d.min_cgpa = $min_cgpa,
            d.max_backlogs = $max_backlogs,
            d.updated_at = datetime()

        // Link Posting Company
        WITH d
        MATCH (c:Company {id: $company_id})
        MERGE (c)-[:POSTS]->(d)

        // Sync Programmes
        WITH d
        OPTIONAL MATCH (d)-[rp:FOR_PROGRAMME]->(old_p:Programme)
        WHERE NOT old_p.name IN $programmes
        DELETE rp

        WITH d
        UNWIND $programmes AS prog_name
        MERGE (p:Programme {name: prog_name})
        MERGE (d)-[:FOR_PROGRAMME]->(p)

        // Sync Skills
        WITH d
        OPTIONAL MATCH (d)-[rs:REQUIRES]->(old_s:Skill)
        WHERE NOT old_s.normalized_name IN $skills
        DELETE rs

        WITH d
        UNWIND $skills AS skill_norm
        MERGE (sk:Skill {normalized_name: skill_norm})
        ON CREATE SET sk.name = skill_norm, sk.category = 'General', sk.created_at = datetime()
        MERGE (d)-[:REQUIRES]->(sk)

        RETURN d.id AS id, d.title AS title, d.status AS status
        """
        params = {
            "drive_id": str(drive_id),
            "company_id": str(company_id),
            "title": title.strip(),
            "role_type": role_type,
            "salary_package": salary_package,
            "status": status,
            "min_cgpa": float(min_cgpa),
            "max_backlogs": int(max_backlogs),
            "programmes": [p.strip() for p in allowed_programmes if p.strip()],
            "skills": normalized_skills,
        }
        res = await self.execute_write(query, params)
        return res[0] if res else {}

    async def get_drive_details_graph(self, drive_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves graph information for a drive including required skills, programmes, and company."""
        query = """
        MATCH (d:PlacementDrive {id: $drive_id})
        OPTIONAL MATCH (c:Company)-[:POSTS]->(d)
        OPTIONAL MATCH (d)-[:FOR_PROGRAMME]->(p:Programme)
        OPTIONAL MATCH (d)-[:REQUIRES]->(s:Skill)
        RETURN 
            d.id AS id,
            d.title AS title,
            d.role_type AS role_type,
            d.salary_package AS salary_package,
            d.status AS status,
            d.min_cgpa AS min_cgpa,
            d.max_backlogs AS max_backlogs,
            c.id AS company_id,
            c.name AS company_name,
            collect(DISTINCT p.name) AS allowed_programmes,
            collect(DISTINCT s.normalized_name) AS required_skills
        """
        res = await self.execute_read(query, {"drive_id": str(drive_id)})
        return res[0] if res else None

    async def delete_drive_node(self, drive_id: str) -> None:
        """Detaches and deletes a PlacementDrive node from the graph."""
        query = """
        MATCH (d:PlacementDrive {id: $drive_id})
        DETACH DELETE d
        """
        await self.execute_write(query, {"drive_id": str(drive_id)})