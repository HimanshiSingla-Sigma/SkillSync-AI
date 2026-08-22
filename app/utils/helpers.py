import os
import uuid
import aiofiles
from fastapi import UploadFile
from app.core.config import settings
from app.utils.validators import validate_file_extension


async def save_uploaded_file(upload_file: UploadFile) -> str:
    """Saves uploaded multipart file to the configured uploads folder with a unique UUID filename."""
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    extension = validate_file_extension(
        upload_file.filename or "", settings.ALLOWED_EXTENSIONS
    )
    unique_filename = f"{uuid.uuid4().hex}.{extension}"
    target_path = os.path.join(settings.UPLOAD_DIR, unique_filename)

    async with aiofiles.open(target_path, "wb") as out_file:
        while content := await upload_file.read(1024 * 1024):  # 1MB buffer
            await out_file.write(content)

    await upload_file.seek(0)
    return target_path