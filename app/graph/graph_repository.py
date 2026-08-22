from typing import Any, Dict, List, Optional
from neo4j.exceptions import Neo4jError
from app.core.neo4j import Neo4jManager
from app.core.logging import logger


class GraphRepository:
    """Base repository providing parameterized, transaction-safe Cypher query execution."""

    @staticmethod
    async def execute_write(query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Executes a parameterized write query within an explicit asynchronous session."""
        driver = Neo4jManager.get_driver()
        try:
            async with driver.session() as session:
                result = await session.run(query, parameters or {})
                data = await result.data()
                return data
        except Neo4jError as e:
            logger.error(f"Neo4j Cypher write error: {str(e)} | Query: {query} | Params: {parameters}")
            raise e

    @staticmethod
    async def execute_read(query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Executes a parameterized read query within an explicit asynchronous session."""
        driver = Neo4jManager.get_driver()
        try:
            async with driver.session() as session:
                result = await session.run(query, parameters or {})
                data = await result.data()
                return data
        except Neo4jError as e:
            logger.error(f"Neo4j Cypher read error: {str(e)} | Query: {query} | Params: {parameters}")
            raise e