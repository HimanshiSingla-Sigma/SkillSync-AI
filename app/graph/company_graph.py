from typing import Any, Dict, Optional
from app.graph.graph_repository import GraphRepository


class CompanyGraphRepository(GraphRepository):
    """Manages (Company) nodes in the knowledge graph."""

    async def upsert_company(
        self,
        company_id: str,
        name: str,
        email: str,
        industry: str,
        location: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Creates or updates a Company node."""
        query = """
        MERGE (c:Company {id: $company_id})
        ON CREATE SET 
            c.name = $name,
            c.email = $email,
            c.industry = $industry,
            c.location = $location,
            c.created_at = datetime()
        ON MATCH SET 
            c.name = $name,
            c.email = $email,
            c.industry = $industry,
            c.location = $location,
            c.updated_at = datetime()
        RETURN c.id AS id, c.name AS name, c.industry AS industry
        """
        params = {
            "company_id": str(company_id),
            "name": name.strip(),
            "email": email.strip().lower(),
            "industry": industry.strip(),
            "location": location or "Not Specified",
        }
        res = await self.execute_write(query, params)
        return res[0] if res else {}

    async def delete_company_node(self, company_id: str) -> None:
        """Detaches and deletes a Company node from the graph."""
        query = """
        MATCH (c:Company {id: $company_id})
        DETACH DELETE c
        """
        await self.execute_write(query, {"company_id": str(company_id)})