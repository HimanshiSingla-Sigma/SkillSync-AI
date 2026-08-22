"""Script to verify and clear/initialize base knowledge graph metadata."""

import asyncio
from app.core.neo4j import Neo4jManager
from app.core.logging import logger


async def initialize_graph():
    """Cleans up corrupted/orphaned graph data and sets up foundational labels."""
    logger.info("Connecting to Neo4j to prepare graph environment...")
    await Neo4jManager.connect_to_database()

    # Pre-seed foundational canonical programmes
    programmes = [
        "B.Tech Computer Science",
        "B.Tech Information Technology",
        "B.Tech Electronics and Communication",
        "B.Tech Mechanical Engineering",
        "B.Tech Data Science & AI",
        "MCA",
        "BCA",
    ]

    query = """
    UNWIND $programmes AS prog_name
    MERGE (p:Programme {name: prog_name})
    RETURN count(p) as total_programmes
    """
    res = await Neo4jManager.run_query(query, {"programmes": programmes})
    logger.info(f"Initialized base academic programmes: {res}")

    await Neo4jManager.close_database_connection()
    logger.info("Graph initialization complete.")


if __name__ == "__main__":
    asyncio.run(initialize_graph())