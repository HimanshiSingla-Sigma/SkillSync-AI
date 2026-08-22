from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.mongodb import MongoDBManager
from app.models.placement_drive import PlacementDriveModel


class DriveRepository:
    """Handles all MongoDB persistence for Placement Drives."""

    def __init__(self, db: Optional[AsyncIOMotorDatabase] = None):
        self._db = db

    @property
    def collection(self):
        db = self._db if self._db is not None else MongoDBManager.get_database()
        return db["placement_drives"]

    def _serialize_doc(self, doc: Optional[Dict[str, Any]]) -> Optional[PlacementDriveModel]:
        if not doc:
            return None
        doc["_id"] = str(doc["_id"])
        return PlacementDriveModel(**doc)

    async def create(self, drive: PlacementDriveModel) -> PlacementDriveModel:
        doc = drive.model_dump(by_alias=True, exclude={"id"})
        doc["created_at"] = datetime.now(timezone.utc)
        doc["updated_at"] = datetime.now(timezone.utc)
        result = await self.collection.insert_one(doc)
        doc["_id"] = str(result.inserted_id)
        return PlacementDriveModel(**doc)

    async def find_by_id(self, drive_id: str) -> Optional[PlacementDriveModel]:
        if not ObjectId.is_valid(drive_id):
            return None
        doc = await self.collection.find_one({"_id": ObjectId(drive_id)})
        return self._serialize_doc(doc)

    async def find_by_company_id(self, company_id: str) -> List[PlacementDriveModel]:
        cursor = self.collection.find({"company_id": company_id})
        drives = []
        async for doc in cursor:
            drives.append(self._serialize_doc(doc))
        return [d for d in drives if d is not None]

    async def update(self, drive_id: str, update_data: Dict[str, Any]) -> Optional[PlacementDriveModel]:
        if not ObjectId.is_valid(drive_id):
            return None
        update_data["updated_at"] = datetime.now(timezone.utc)
        await self.collection.update_one(
            {"_id": ObjectId(drive_id)},
            {"$set": update_data},
        )
        return await self.find_by_id(drive_id)

    async def list_all(
        self,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[PlacementDriveModel]:
        query: Dict[str, Any] = {}
        if status:
            query["status"] = status
        cursor = self.collection.find(query).skip(skip).limit(limit)
        drives = []
        async for doc in cursor:
            drives.append(self._serialize_doc(doc))
        return [d for d in drives if d is not None]

    async def delete(self, drive_id: str) -> bool:
        if not ObjectId.is_valid(drive_id):
            return False
        result = await self.collection.delete_one({"_id": ObjectId(drive_id)})
        return result.deleted_count > 0