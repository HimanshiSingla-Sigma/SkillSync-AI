import os
from typing import Optional
from app.models.resume import ResumeModel
from app.models.student import StudentModel
from app.resume_processing.text_extractor import TextExtractor
from app.resume_processing.information_extractor import InformationExtractor
from app.resume_processing.resume_normalizer import ResumeNormalizer
from app.repositories.student_repository import StudentRepository
from app.services.resume_service import ResumeService
from app.sync.graph_sync_service import GraphSyncService, graph_sync_service
from app.core.logging import logger


class ResumeParserEngine:
    """
    Complete Resume Ingestion Engine:
    File upload -> Extraction -> Entity Parsing -> Storage -> Sync
    """

    def __init__(
        self,
        resume_service: Optional[ResumeService] = None,
        student_repo: Optional[StudentRepository] = None,
        sync_service: Optional[GraphSyncService] = None,
    ):
        self.resume_service = resume_service or ResumeService()
        self.student_repo = student_repo or StudentRepository()
        self.sync = sync_service or graph_sync_service

    async def parse_and_save(
        self,
        student_id: str,
        file_path: str,
        file_name: str,
        file_type: str,
    ) -> ResumeModel:
        """Executes full resume parsing pipeline and automatically updates student profile."""
        logger.info(f"Starting resume processing for Student ID: {student_id} from {file_path}")

        # 1. Text Extraction
        raw_text = TextExtractor.extract(file_path=file_path, file_type=file_type)
        cleaned_text = ResumeNormalizer.clean_text(raw_text)

        # 2. Information Extraction
        extracted_data = InformationExtractor.extract_structured_sections(cleaned_text)

        # 3. Create Resume Document
        resume_doc = ResumeModel(
            student_id=student_id,
            file_name=file_name,
            file_path=file_path,
            file_type=file_type,
            raw_text=cleaned_text,
            extracted_name=extracted_data.get("name"),
            extracted_email=extracted_data.get("email"),
            extracted_phone=extracted_data.get("phone"),
            extracted_education=extracted_data.get("education", []),
            extracted_skills=extracted_data.get("skills", []),
            extracted_projects=extracted_data.get("projects", []),
            extracted_experience=extracted_data.get("experience", []),
            extracted_certifications=extracted_data.get("certifications", []),
            parsing_metadata={"character_count": len(cleaned_text), "file_type": file_type},
        )

        saved_resume = await self.resume_service.save_resume_record(resume_doc)

        # 4. Auto-update Student profile with extracted details if missing
        student = await self.student_repo.find_by_id(student_id)
        if student:
            updated_skills = list(set(student.skills + extracted_data.get("skills", [])))
            update_payload = {"skills": updated_skills}

            if extracted_data.get("education"):
                edu = extracted_data["education"][0]
                if edu.cgpa and student.profile.cgpa == 0.0:
                    student.profile.cgpa = edu.cgpa
                if edu.branch and not student.profile.branch:
                    student.profile.branch = edu.branch
                if edu.degree and not student.profile.programme:
                    student.profile.programme = f"{edu.degree} {edu.branch or ''}".strip()
                if edu.graduation_year:
                    student.profile.graduation_year = edu.graduation_year
                update_payload["profile"] = student.profile.model_dump()

            updated_student = await self.student_repo.update(student_id, update_payload)
            # Sync with Neo4j Knowledge Graph
            if updated_student:
                await self.sync.sync_student(updated_student)

        logger.info(f"Successfully processed resume for Student ID: {student_id}")
        return resume_doc