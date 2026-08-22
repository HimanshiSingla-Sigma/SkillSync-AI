import os
import aiofiles
from typing import Any, Dict, Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.config import settings
from app.core.mongodb import MongoDBManager
from app.models.resume import ResumeModel, ExtractedEducation, ExtractedProject, ExtractedExperience
from app.repositories.student_repository import StudentRepository
from app.sync.graph_sync_service import GraphSyncService, graph_sync_service
from app.services.skill_extraction_service import SkillExtractionService
from app.schemas.resume_schema import (
    ResumeResponse,
    ResumeCorrectionRequest,
    ExtractedEducationSchema,
    ExtractedProjectSchema,
    ExtractedExperienceSchema,
)
from app.utils.exceptions import BadRequestException, NotFoundException


class ResumeService:
    """Handles resume document storage, extraction updates, manual corrections, and sync."""

    def __init__(
        self,
        db: Optional[AsyncIOMotorDatabase] = None,
        student_repo: Optional[StudentRepository] = None,
        sync_service: Optional[GraphSyncService] = None,
    ):
        self._db = db
        self.student_repo = student_repo or StudentRepository()
        self.sync = sync_service or graph_sync_service

    @property
    def collection(self):
        db = self._db if self._db is not None else MongoDBManager.get_database()
        return db["resumes"]

    def _to_response_dto(self, doc: ResumeModel) -> ResumeResponse:
        return ResumeResponse(
            id=str(doc.id),
            student_id=doc.student_id,
            file_name=doc.file_name,
            file_type=doc.file_type,
            raw_text=doc.raw_text,
            extracted_name=doc.extracted_name,
            extracted_email=doc.extracted_email,
            extracted_phone=doc.extracted_phone,
            extracted_education=[
                ExtractedEducationSchema(**e.model_dump()) for e in doc.extracted_education
            ],
            extracted_skills=doc.extracted_skills,
            extracted_projects=[
                ExtractedProjectSchema(**p.model_dump()) for p in doc.extracted_projects
            ],
            extracted_experience=[
                ExtractedExperienceSchema(**x.model_dump()) for x in doc.extracted_experience
            ],
            extracted_certifications=doc.extracted_certifications,
            uploaded_at=doc.uploaded_at,
            updated_at=doc.updated_at,
        )

    async def get_by_student_id(self, student_id: str) -> Optional[ResumeResponse]:
        doc = await self.collection.find_one({"student_id": student_id})
        if not doc:
            return None
        doc["_id"] = str(doc["_id"])
        return self._to_response_dto(ResumeModel(**doc))

    async def save_resume_record(self, resume_doc: ResumeModel) -> ResumeResponse:
        data = resume_doc.model_dump(by_alias=True, exclude={"id"})
        result = await self.collection.insert_one(data)
        data["_id"] = str(result.inserted_id)

        # Update student record with active resume ID
        await self.student_repo.attach_resume(resume_doc.student_id, str(result.inserted_id))

        return self._to_response_dto(ResumeModel(**data))

    async def correct_resume_data(
        self,
        student_id: str,
        req: ResumeCorrectionRequest,
    ) -> ResumeResponse:
        """Allows student to manually edit and correct parsed resume entities."""
        doc = await self.collection.find_one({"student_id": student_id})
        if not doc:
            raise NotFoundException("No resume profile found for this student.")

        update_fields: Dict[str, Any] = req.model_dump(exclude_unset=True)

        if "extracted_skills" in update_fields and update_fields["extracted_skills"]:
            update_fields["extracted_skills"] = SkillExtractionService.extract_and_normalize(
                update_fields["extracted_skills"]
            )
            # Sync corrected skills directly to Student profile
            await self.student_repo.update_skills(student_id, update_fields["extracted_skills"])
            student = await self.student_repo.find_by_id(student_id)
            if student:
                await self.sync.sync_student(student)

        await self.collection.update_one(
            {"_id": doc["_id"]},
            {"$set": update_fields},
        )

        updated = await self.collection.find_one({"_id": doc["_id"]})
        updated["_id"] = str(updated["_id"])
        return self._to_response_dto(ResumeModel(**updated))