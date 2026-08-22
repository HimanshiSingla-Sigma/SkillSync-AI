import os
import re
from typing import List
from bson import ObjectId
from app.utils.exceptions import BadRequestException


def validate_object_id(id_str: str, entity_name: str = "Entity") -> str:
    """Validates whether a string is a 24-character hex MongoDB ObjectId."""
    if not id_str or not ObjectId.is_valid(id_str):
        raise BadRequestException(f"Invalid {entity_name} ID format: '{id_str}'")
    return id_str


def validate_file_extension(filename: str, allowed_extensions: List[str]) -> str:
    """Validates allowed resume document formats."""
    ext = os.path.splitext(filename)[1].replace(".", "").lower()
    if ext not in allowed_extensions:
        raise BadRequestException(
            f"Unsupported file format '{ext}'. Allowed formats: {', '.join(allowed_extensions)}"
        )
    return ext


def validate_email_format(email: str) -> str:
    """Validates standard email format."""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(pattern, email):
        raise BadRequestException(f"Malformed email address: '{email}'")
    return email.lower().strip()