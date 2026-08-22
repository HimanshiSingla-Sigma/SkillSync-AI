"""Script to apply unique constraints and performance indexes on Neo4j."""

import asyncio
from app.core.neo4j import Neo4jManager
from app.core.logging import logger


async def apply_neo4j_constraints():
    """Initializes schema constraints and uniqueness guarantees in Neo4j."""
    logger.info("Initializing Neo4j unique constraints and indexes...")
    await Neo4jManager.connect_to_database()

    constraints = [
        "CREATE CONSTRAINT student_id_unique IF NOT EXISTS FOR (s:Student) REQUIRE s.id IS UNIQUE",
        "CREATE CONSTRAINT student_email_unique IF NOT EXISTS FOR (s:Student) REQUIRE s.email IS UNIQUE",
        "CREATE CONSTRAINT company_id_unique IF NOT EXISTS FOR (c:Company) REQUIRE c.id IS UNIQUE",
        "CREATE CONSTRAINT company_email_unique IF NOT EXISTS FOR (c:Company) REQUIRE c.email IS UNIQUE",
        "CREATE CONSTRAINT drive_id_unique IF NOT EXISTS FOR (d:PlacementDrive) REQUIRE d.id IS UNIQUE",
        "CREATE CONSTRAINT skill_normalized_name_unique IF NOT EXISTS FOR (sk:Skill) REQUIRE sk.normalized_name IS UNIQUE",
        "CREATE CONSTRAINT programme_name_unique IF NOT EXISTS FOR (p:Programme) REQUIRE p.name IS UNIQUE",
    ]

    for constraint_cypher in constraints:
        try:
            await Neo4jManager.run_query(constraint_cypher)
            logger.info(f"Successfully executed: {constraint_cypher}")
        except Exception as e:
            logger.warning(f"Notice on executing '{constraint_cypher}': {e}")

    await Neo4jManager.close_database_connection()
    logger.info("Neo4j constraints and indexes applied successfully.")


if __name__ == "__main__":
    asyncio.run(apply_neo4j_constraints())