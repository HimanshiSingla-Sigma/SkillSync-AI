from typing import Any, Dict, List
from app.graph.graph_repository import GraphRepository
from app.core.logging import logger


class SkillGraphRepository(GraphRepository):
    """Manages (Skill) nodes and normalization queries in the knowledge graph."""

    async def merge_skill(self, name: str, normalized_name: str, category: str = "General") -> Dict[str, Any]:
        """Idempotently creates or updates a canonical Skill node."""
        query = """
        MERGE (s:Skill {normalized_name: $normalized_name})
        ON CREATE SET 
            s.name = $name,
            s.category = $category,
            s.created_at = datetime()
        ON MATCH SET 
            s.name = $name,
            s.category = $category,
            s.updated_at = datetime()
        RETURN s.normalized_name AS normalized_name, s.name AS name, s.category AS category
        """
        params = {
            "name": name.strip(),
            "normalized_name": normalized_name.strip().lower(),
            "category": category,
        }
        res = await self.execute_write(query, params)
        return res[0] if res else {}

    async def get_all_skills(self) -> List[Dict[str, Any]]:
        query = """
        MATCH (s:Skill)
        RETURN s.name AS name, s.normalized_name AS normalized_name, s.category AS category
        ORDER BY s.normalized_name ASC
        """
        return await self.execute_read(query)