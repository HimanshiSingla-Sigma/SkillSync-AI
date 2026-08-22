import os
from app.core.mongodb import MongoDBManager
from app.core.neo4j import Neo4jManager
from app.core.config import settings
from app.core.logging import logger


async def init_databases() -> None:
    """Initializes and verifies connections to both MongoDB and Neo4j databases."""
    logger.info("Initializing multi-database persistence layer...")

    # Ensure uploads directory exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    await MongoDBManager.connect_to_database()
    await Neo4jManager.connect_to_database()

    # Create MongoDB unique indexes
    db = MongoDBManager.get_database()
    await db["students"].create_index("email", unique=True)
    await db["companies"].create_index("email", unique=True)
    await db["applications"].create_index(
        [("student_id", 1), ("drive_id", 1)], unique=True
    )
    await db["skills"].create_index("normalized_name", unique=True)

    logger.info("Database connections and indexes initialized successfully.")


async def close_databases() -> None:
    """Gracefully shuts down all active database connections."""
    logger.info("Closing multi-database persistence connections...")
    await MongoDBManager.close_database_connection()
    await Neo4jManager.close_database_connection()
    logger.info("All database connections terminated.")