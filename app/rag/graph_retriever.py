from typing import Any, Dict, List, Optional
from app.graph.graph_repository import GraphRepository
from app.core.logging import logger


class GraphRetriever(GraphRepository):
    """
    Executes precise multi-hop graph traversals in Neo4j to retrieve factual
    context regarding students, companies, drives, skills, and eligibility paths.
    """

    async def retrieve_student_profile(self, student_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves student node, enrolled programme, and linked skills."""
        query = """
        MATCH (s:Student {id: $student_id})
        OPTIONAL MATCH (s)-[:STUDIES]->(p:Programme)
        OPTIONAL MATCH (s)-[:HAS_SKILL]->(sk:Skill)
        RETURN 
            s.id AS student_id,
            s.full_name AS full_name,
            s.email AS email,
            s.cgpa AS cgpa,
            s.backlogs AS backlogs,
            s.graduation_year AS graduation_year,
            s.branch AS branch,
            p.name AS programme,
            collect(DISTINCT sk.normalized_name) AS skills
        """
        records = await self.execute_read(query, {"student_id": str(student_id)})
        return records[0] if records else None

    async def retrieve_drive_profile(self, drive_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves placement drive details, hosting company, required skills, and programmes."""
        query = """
        MATCH (d:PlacementDrive {id: $drive_id})
        OPTIONAL MATCH (c:Company)-[:POSTS]->(d)
        OPTIONAL MATCH (d)-[:FOR_PROGRAMME]->(p:Programme)
        OPTIONAL MATCH (d)-[:REQUIRES]->(sk:Skill)
        RETURN 
            d.id AS drive_id,
            d.title AS title,
            d.role_type AS role_type,
            d.salary_package AS salary_package,
            d.min_cgpa AS min_cgpa,
            d.max_backlogs AS max_backlogs,
            c.id AS company_id,
            c.name AS company_name,
            collect(DISTINCT p.name) AS allowed_programmes,
            collect(DISTINCT sk.normalized_name) AS required_skills
        """
        records = await self.execute_read(query, {"drive_id": str(drive_id)})
        return records[0] if records else None

    async def find_drive_by_company_or_title(self, keyword: str) -> Optional[Dict[str, Any]]:
        """Fuzzy matches a placement drive or company name across the graph."""
        query = """
        MATCH (d:PlacementDrive)
        OPTIONAL MATCH (c:Company)-[:POSTS]->(d)
        WHERE toLower(d.title) CONTAINS toLower($keyword) 
           OR toLower(c.name) CONTAINS toLower($keyword)
        OPTIONAL MATCH (d)-[:FOR_PROGRAMME]->(p:Programme)
        OPTIONAL MATCH (d)-[:REQUIRES]->(sk:Skill)
        RETURN 
            d.id AS drive_id,
            d.title AS title,
            d.role_type AS role_type,
            d.salary_package AS salary_package,
            d.min_cgpa AS min_cgpa,
            d.max_backlogs AS max_backlogs,
            c.id AS company_id,
            c.name AS company_name,
            collect(DISTINCT p.name) AS allowed_programmes,
            collect(DISTINCT sk.normalized_name) AS required_skills
        LIMIT 1
        """
        records = await self.execute_read(query, {"keyword": keyword.strip()})
        return records[0] if records else None

    async def retrieve_student_drive_graph_context(
        self, student_id: str, drive_id: str
    ) -> Dict[str, Any]:
        """
        Retrieves graph comparison between a student and a placement drive:
        - Student profile & skills
        - Drive requirements & criteria
        - Intersecting skills (matched)
        - Missing skills (unmatched requirements)
        """
        query = """
        MATCH (s:Student {id: $student_id})
        MATCH (d:PlacementDrive {id: $drive_id})
        OPTIONAL MATCH (c:Company)-[:POSTS]->(d)
        OPTIONAL MATCH (s)-[:STUDIES]->(p_student:Programme)
        OPTIONAL MATCH (d)-[:FOR_PROGRAMME]->(p_drive:Programme)
        
        // Match possessed skills
        OPTIONAL MATCH (s)-[:HAS_SKILL]->(sk_student:Skill)
        WITH s, d, c, p_student, collect(DISTINCT p_drive.name) AS allowed_programmes, collect(DISTINCT sk_student.normalized_name) AS student_skills
        
        // Match required skills
        OPTIONAL MATCH (d)-[:REQUIRES]->(sk_req:Skill)
        WITH s, d, c, p_student, allowed_programmes, student_skills, collect(DISTINCT sk_req.normalized_name) AS required_skills
        
        // Overlap calculation in Cypher
        RETURN 
            s.id AS student_id,
            s.full_name AS student_name,
            s.cgpa AS student_cgpa,
            s.backlogs AS student_backlogs,
            s.graduation_year AS student_graduation_year,
            p_student.name AS student_programme,
            student_skills,
            d.id AS drive_id,
            d.title AS drive_title,
            d.min_cgpa AS min_cgpa,
            d.max_backlogs AS max_backlogs,
            c.name AS company_name,
            allowed_programmes,
            required_skills,
            [x IN required_skills WHERE x IN student_skills] AS matched_skills,
            [x IN required_skills WHERE NOT x IN student_skills] AS missing_skills
        """
        records = await self.execute_read(
            query, {"student_id": str(student_id), "drive_id": str(drive_id)}
        )
        return records[0] if records else {}

    async def retrieve_suitable_drives_for_student(
        self, student_id: str, limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Retrieves top placement drives where the student meets criteria and matches skills."""
        query = """
        MATCH (s:Student {id: $student_id})
        MATCH (d:PlacementDrive {status: 'PUBLISHED'})
        OPTIONAL MATCH (c:Company)-[:POSTS]->(d)
        OPTIONAL MATCH (s)-[:HAS_SKILL]->(sk_s:Skill)
        OPTIONAL MATCH (d)-[:REQUIRES]->(sk_d:Skill)
        
        WITH s, d, c, collect(DISTINCT sk_s.normalized_name) AS student_skills, collect(DISTINCT sk_d.normalized_name) AS required_skills
        
        WITH d, c, student_skills, required_skills,
             [x IN required_skills WHERE x IN student_skills] AS matched_skills,
             [x IN required_skills WHERE NOT x IN student_skills] AS missing_skills
             
        WHERE s.cgpa >= d.min_cgpa AND s.backlogs <= d.max_backlogs
        
        RETURN 
            d.id AS drive_id,
            d.title AS drive_title,
            d.salary_package AS salary_package,
            c.name AS company_name,
            required_skills,
            matched_skills,
            missing_skills,
            CASE WHEN size(required_skills) = 0 THEN 100.0
                 ELSE (toFloat(size(matched_skills)) / toFloat(size(required_skills))) * 100.0 END AS match_pct
        ORDER BY match_pct DESC
        LIMIT $limit
        """
        return await self.execute_read(
            query, {"student_id": str(student_id), "limit": limit}
        )