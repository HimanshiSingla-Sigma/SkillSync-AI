from typing import Optional
from app.graph.company_graph import CompanyGraphRepository
from app.models.company import CompanyModel
from app.core.logging import logger


class CompanySync:
    """Synchronizes MongoDB Company entities into Neo4j."""

    def __init__(self, graph_repo: Optional[CompanyGraphRepository] = None):
        self.graph_repo = graph_repo or CompanyGraphRepository()

    async def sync(self, company: CompanyModel) -> None:
        if not company.id:
            logger.warning("Skipping Company sync: Missing company ID.")
            return

        try:
            await self.graph_repo.upsert_company(
                company_id=str(company.id),
                name=company.name,
                email=company.email,
                industry=company.industry,
                location=company.location,
            )
            logger.info(f"Synchronized company '{company.name}' (ID: {company.id}) to Neo4j graph.")
        except Exception as e:
            logger.error(f"Failed to sync Company {company.id} to Neo4j: {str(e)}")
            raise e

    async def delete(self, company_id: str) -> None:
        try:
            await self.graph_repo.delete_company_node(str(company_id))
            logger.info(f"Deleted company ID '{company_id}' from Neo4j graph.")
        except Exception as e:
            logger.error(f"Failed to delete Company {company_id} from Neo4j: {str(e)}")
            raise e