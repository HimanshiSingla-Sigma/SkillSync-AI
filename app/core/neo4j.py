from typing import Any, Dict, List, Optional
from neo4j import AsyncGraphDatabase, AsyncDriver, AsyncSession
from app.core.config import settings
from app.core.logging import logger


class Neo4jManager:
    driver: Optional[AsyncDriver] = None

    @classmethod
    async def connect_to_database(cls) -> None:
        """Establishes connection pool with Neo4j Bolt driver."""
        try:
            logger.info(f"Connecting to Neo4j instance at {settings.NEO4J_URI}...")
            cls.driver = AsyncGraphDatabase.driver(
                settings.NEO4J_URI,
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
                max_connection_pool_size=settings.NEO4J_MAX_CONNECTION_POOL_SIZE,
            )
            # Verify connectivity
            await cls.driver.verify_connectivity()
            logger.info("Successfully connected to Neo4j Graph Database.")
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {str(e)}")
            raise e

    @classmethod
    async def close_database_connection(cls) -> None:
        """Closes the Neo4j driver connection pool."""
        if cls.driver:
            logger.info("Closing Neo4j driver connection pool...")
            await cls.driver.close()
            cls.driver = None
            logger.info("Neo4j connection closed.")

    @classmethod
    def get_driver(cls) -> AsyncDriver:
        """Retrieves the active Neo4j driver instance."""
        if cls.driver is None:
            raise RuntimeError(
                "Neo4j driver not initialized. Call connect_to_database first."
            )
        return cls.driver

    @classmethod
    async def run_query(
        cls, query: str, parameters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Executes a parameterized Cypher query and returns the record dictionaries."""
        driver = cls.get_driver()
        async with driver.session() as session:
            result = await session.run(query, parameters or {})
            records = await result.data()
            return records


async def get_neo4j_session() -> AsyncSession:
    """Dependency injector yielding an async Neo4j session."""
    driver = Neo4jManager.get_driver()
    async with driver.session() as session:
        yield session