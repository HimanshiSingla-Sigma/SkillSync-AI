from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.mongodb import MongoDBManager
from app.models.company import CompanyModel


class CompanyRepository:
    """Handles all MongoDB read/write persistence for Company entities."""

    def __init__(self, db: Optional[AsyncIOMotorDatabase] = None):
        self._db = db

    @property
    def collection(self):
        db = self._db if self._db is not None else MongoDBManager.get_database()
        return db["companies"]

    def _serialize_doc(self, doc: Optional[Dict[str, Any]]) -> Optional[CompanyModel]:
        if not doc:
            return None
        doc["_id"] = str(doc["_id"])
        return CompanyModel(**doc)

    async def create(self, company: CompanyModel) -> CompanyModel:
        doc = company.model_dump(by_alias=True, exclude={"id"})
        doc["created_at"] = datetime.now(timezone.utc)
        doc["updated_at"] = datetime.now(timezone.utc)
        result = await self.collection.insert_one(doc)
        doc["_id"] = str(result.inserted_id)
        return CompanyModel(**doc)

    async def find_by_id(self, company_id: str) -> Optional[CompanyModel]:
        if not ObjectId.is_valid(company_id):
            return None
        doc = await self.collection.find_one({"_id": ObjectId(company_id)})
        return self._serialize_doc(doc)

    async def find_by_email(self, email: str) -> Optional[CompanyModel]:
        doc = await self.collection.find_one({"email": email.strip().lower()})
        return self._serialize_doc(doc)

    async def update(self, company_id: str, update_data: Dict[str, Any]) -> Optional[CompanyModel]:
        if not ObjectId.is_valid(company_id):
            return None
        update_data["updated_at"] = datetime.now(timezone.utc)
        await self.collection.update_one(
            {"_id": ObjectId(company_id)},
            {"$set": update_data},
        )
        return await self.find_by_id(company_id)

    async def list_all(self, skip: int = 0, limit: int = 100) -> List[CompanyModel]:
        cursor = self.collection.find({}).skip(skip).limit(limit)
        companies = []
        async for doc in cursor:
            companies.append(self._serialize_doc(doc))
        return [c for c in companies if c is not None]

    async def delete(self, company_id: str) -> bool:
        if not ObjectId.is_valid(company_id):
            return False
        result = await self.collection.delete_one({"_id": ObjectId(company_id)})
        return result.deleted_count > 0