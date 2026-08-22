from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.core.config import settings
from app.core.logging import logger


class MongoDBManager:
    client: Optional[AsyncIOMotorClient] = None
    db: Optional[AsyncIOMotorDatabase] = None

    @classmethod
    async def connect_to_database(cls) -> None:
        """Establishes MongoDB connection pool with Motor."""
        try:
            logger.info(f"Connecting to MongoDB at {settings.MONGODB_URI}...")
            cls.client = AsyncIOMotorClient(
                settings.MONGODB_URI,
                minPoolSize=settings.MONGODB_MIN_POOL_SIZE,
                maxPoolSize=settings.MONGODB_MAX_POOL_SIZE,
            )
            cls.db = cls.client[settings.MONGODB_DB_NAME]
            # Ping database to verify connection
            await cls.client.admin.command("ping")
            logger.info(
                f"Successfully connected to MongoDB Database: {settings.MONGODB_DB_NAME}"
            )
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise e

    @classmethod
    async def close_database_connection(cls) -> None:
        """Closes MongoDB connection pool."""
        if cls.client:
            logger.info("Closing MongoDB connection pool...")
            cls.client.close()
            cls.client = None
            cls.db = None
            logger.info("MongoDB connection closed.")

    @classmethod
    def get_database(cls) -> AsyncIOMotorDatabase:
        """Retrieves the active MongoDB database instance."""
        if cls.db is None:
            raise RuntimeError(
                "MongoDB database not initialized. Call connect_to_database first."
            )
        return cls.db


async def get_mongo_db() -> AsyncIOMotorDatabase:
    """Dependency injector for obtaining async MongoDB database reference."""
    return MongoDBManager.get_database()