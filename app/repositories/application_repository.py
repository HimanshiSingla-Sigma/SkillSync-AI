from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.mongodb import MongoDBManager
from app.models.application import ApplicationModel, ApplicationStatusHistory


class ApplicationRepository:
    """Handles all MongoDB read/write persistence for Applications."""

    def __init__(self, db: Optional[AsyncIOMotorDatabase] = None):
        self._db = db

    @property
    def collection(self):
        db = self._db if self._db is not None else MongoDBManager.get_database()
        return db["applications"]

    def _serialize_doc(self, doc: Optional[Dict[str, Any]]) -> Optional[ApplicationModel]:
        if not doc:
            return None
        doc["_id"] = str(doc["_id"])
        return ApplicationModel(**doc)

    async def create(self, application: ApplicationModel) -> ApplicationModel:
        doc = application.model_dump(by_alias=True, exclude={"id"})
        doc["created_at"] = datetime.now(timezone.utc)
        doc["updated_at"] = datetime.now(timezone.utc)
        result = await self.collection.insert_one(doc)
        doc["_id"] = str(result.inserted_id)
        return ApplicationModel(**doc)

    async def find_by_id(self, application_id: str) -> Optional[ApplicationModel]:
        if not ObjectId.is_valid(application_id):
            return None
        doc = await self.collection.find_one({"_id": ObjectId(application_id)})
        return self._serialize_doc(doc)

    async def find_by_student_and_drive(
        self, student_id: str, drive_id: str
    ) -> Optional[ApplicationModel]:
        doc = await self.collection.find_one(
            {"student_id": student_id, "drive_id": drive_id}
        )
        return self._serialize_doc(doc)

    async def find_by_student_id(self, student_id: str) -> List[ApplicationModel]:
        cursor = self.collection.find({"student_id": student_id})
        apps = []
        async for doc in cursor:
            apps.append(self._serialize_doc(doc))
        return [a for a in apps if a is not None]

    async def find_by_drive_id(self, drive_id: str) -> List[ApplicationModel]:
        cursor = self.collection.find({"drive_id": drive_id})
        apps = []
        async for doc in cursor:
            apps.append(self._serialize_doc(doc))
        return [a for a in apps if a is not None]

    async def find_by_company_id(self, company_id: str) -> List[ApplicationModel]:
        cursor = self.collection.find({"company_id": company_id})
        apps = []
        async for doc in cursor:
            apps.append(self._serialize_doc(doc))
        return [a for a in apps if a is not None]

    async def update_status(
        self, application_id: str, new_status: str, updated_by: str, remarks: Optional[str] = None
    ) -> Optional[ApplicationModel]:
        if not ObjectId.is_valid(application_id):
            return None

        history_entry = ApplicationStatusHistory(
            status=new_status,
            updated_by=updated_by,
            remarks=remarks,
            timestamp=datetime.now(timezone.utc),
        ).model_dump()

        await self.collection.update_one(
            {"_id": ObjectId(application_id)},
            {
                "$set": {
                    "status": new_status,
                    "updated_at": datetime.now(timezone.utc),
                },
                "$push": {"status_history": history_entry},
            },
        )
        return await self.find_by_id(application_id)

    async def delete(self, application_id: str) -> bool:
        if not ObjectId.is_valid(application_id):
            return False
        result = await self.collection.delete_one({"_id": ObjectId(application_id)})
        return result.deleted_count > 0