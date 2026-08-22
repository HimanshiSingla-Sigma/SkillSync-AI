from typing import Any, Dict, List
from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.core.security import decode_access_token
from app.utils.constants import ROLE_ADMIN, ROLE_RECRUITER, ROLE_STUDENT
from app.utils.exceptions import ForbiddenException, UnauthorizedException

security_scheme = HTTPBearer(auto_error=False)


async def get_current_user_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
) -> Dict[str, Any]:
    """Extracts and verifies JWT bearer token from Authorization header."""
    if not credentials or not credentials.credentials:
        raise UnauthorizedException("Missing authentication credentials.")

    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise UnauthorizedException("Invalid, expired, or corrupted token.")

    return payload


async def get_current_user_id(
    payload: Dict[str, Any] = Depends(get_current_user_token_payload),
) -> str:
    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedException("Malformed token: missing subject ID.")
    return str(user_id)


def require_role(allowed_roles: List[str]):
    """Role-based authorization dependency factory."""

    async def role_checker(
        payload: Dict[str, Any] = Depends(get_current_user_token_payload),
    ) -> Dict[str, Any]:
        user_role = payload.get("role")
        if not user_role or user_role not in allowed_roles:
            raise ForbiddenException(
                f"Access denied. Requires one of roles: {allowed_roles}"
            )
        return payload

    return role_checker


# Convenient pre-configured role dependencies
require_student = require_role([ROLE_STUDENT, ROLE_ADMIN])
require_recruiter = require_role([ROLE_RECRUITER, ROLE_ADMIN])
require_admin = require_role([ROLE_ADMIN])