from fastapi import APIRouter, Depends, File, UploadFile, status
from app.api.dependencies import get_current_user_id, require_student
from app.core.config import settings
from app.resume_processing.parser import ResumeParserEngine
from app.schemas.resume_schema import ResumeCorrectionRequest, ResumeResponse
from app.services.resume_service import ResumeService
from app.utils.exceptions import BadRequestException
from app.utils.helpers import save_uploaded_file

router = APIRouter(prefix="/resumes", tags=["Resumes & Parsing"])
resume_service = ResumeService()
parser_engine = ResumeParserEngine()


@router.post(
    "/upload",
    response_model=ResumeResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_student)],
)
async def upload_and_parse_resume(
    file: UploadFile = File(...),
    student_id: str = Depends(get_current_user_id),
):
    """
    Automated Resume Processing Pipeline:
    1. Upload PDF / DOCX
    2. Extract raw text via pdfplumber / python-docx
    3. Heuristically parse name, email, education, and skills
    4. Normalize skills against canonical lexicon
    5. Save resume in MongoDB & auto-update Student profile
    6. Synchronize skills to Neo4j Knowledge Graph
    """
    if not file.filename:
        raise BadRequestException("Missing filename in uploaded resume.")

    file_path = await save_uploaded_file(file)
    file_type = file.filename.split(".")[-1].lower()

    # Parse and synchronize
    resume_doc = await parser_engine.parse_and_save(
        student_id=student_id,
        file_path=file_path,
        file_name=file.filename,
        file_type=file_type,
    )

    return await resume_service.get_by_student_id(student_id)


@router.get(
    "/me",
    response_model=ResumeResponse,
    dependencies=[Depends(require_student)],
)
async def get_my_resume_profile(
    student_id: str = Depends(get_current_user_id),
):
    """Retrieves the latest extracted resume data for the logged-in student."""
    res = await resume_service.get_by_student_id(student_id)
    if not res:
        raise BadRequestException("No resume has been uploaded yet.")
    return res


@router.put(
    "/me/correct",
    response_model=ResumeResponse,
    dependencies=[Depends(require_student)],
)
async def correct_parsed_resume_data(
    req: ResumeCorrectionRequest,
    student_id: str = Depends(get_current_user_id),
):
    """Allows student to manually adjust parsed entities; updates MongoDB and Neo4j graph."""
    return await resume_service.correct_resume_data(student_id, req)