from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.mongodb import MongoDBManager
from app.models.student import StudentModel


class StudentRepository:
    """Handles all MongoDB read/write persistence for Student entities."""

    def __init__(self, db: Optional[AsyncIOMotorDatabase] = None):
        self._db = db

    @property
    def collection(self):
        db = self._db if self._db is not None else MongoDBManager.get_database()
        return db["students"]

    def _serialize_doc(self, doc: Optional[Dict[str, Any]]) -> Optional[StudentModel]:
        if not doc:
            return None
        doc["_id"] = str(doc["_id"])
        return StudentModel(**doc)

    async def create(self, student: StudentModel) -> StudentModel:
        doc = student.model_dump(by_alias=True, exclude={"id"})
        doc["created_at"] = datetime.now(timezone.utc)
        doc["updated_at"] = datetime.now(timezone.utc)
        result = await self.collection.insert_one(doc)
        doc["_id"] = str(result.inserted_id)
        return StudentModel(**doc)

    async def find_by_id(self, student_id: str) -> Optional[StudentModel]:
        if not ObjectId.is_valid(student_id):
            return None
        doc = await self.collection.find_one({"_id": ObjectId(student_id)})
        return self._serialize_doc(doc)

    async def find_by_email(self, email: str) -> Optional[StudentModel]:
        doc = await self.collection.find_one({"email": email.strip().lower()})
        return self._serialize_doc(doc)

    async def update(self, student_id: str, update_data: Dict[str, Any]) -> Optional[StudentModel]:
        if not ObjectId.is_valid(student_id):
            return None
        update_data["updated_at"] = datetime.now(timezone.utc)
        await self.collection.update_one(
            {"_id": ObjectId(student_id)},
            {"$set": update_data},
        )
        return await self.find_by_id(student_id)

    async def update_skills(self, student_id: str, skills: List[str]) -> Optional[StudentModel]:
        if not ObjectId.is_valid(student_id):
            return None
        await self.collection.update_one(
            {"_id": ObjectId(student_id)},
            {
                "$set": {
                    "skills": skills,
                    "updated_at": datetime.now(timezone.utc),
                }
            },
        )
        return await self.find_by_id(student_id)

    async def attach_resume(self, student_id: str, resume_id: str) -> Optional[StudentModel]:
        if not ObjectId.is_valid(student_id):
            return None
        await self.collection.update_one(
            {"_id": ObjectId(student_id)},
            {
                "$set": {
                    "resume_id": resume_id,
                    "updated_at": datetime.now(timezone.utc),
                }
            },
        )
        return await self.find_by_id(student_id)

    async def list_all(self, skip: int = 0, limit: int = 100) -> List[StudentModel]:
        cursor = self.collection.find({}).skip(skip).limit(limit)
        students = []
        async for doc in cursor:
            students.append(self._serialize_doc(doc))
        return [s for s in students if s is not None]

    async def delete(self, student_id: str) -> bool:
        if not ObjectId.is_valid(student_id):
            return False
        result = await self.collection.delete_one({"_id": ObjectId(student_id)})
        return result.deleted_count > 0