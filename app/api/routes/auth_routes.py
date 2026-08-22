from typing import Any, Dict
from fastapi import APIRouter, Query, status
from pydantic import BaseModel, EmailStr
from app.services.otp_service import OTPService

router = APIRouter(prefix="/auth", tags=["Authentication & Email Verification"])


class SendVerificationRequest(BaseModel):
    email: EmailStr


class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str


@router.post("/send-otp", status_code=status.HTTP_200_OK)
@router.post("/send-verification-link", status_code=status.HTTP_200_OK)
async def send_email_verification(req: SendVerificationRequest) -> Dict[str, Any]:
    """Generates a secure verification link & OTP, and dispatches HTML email via SMTP."""
    return await OTPService.send_verification(req.email)


@router.get("/verify-link", status_code=status.HTTP_200_OK)
async def verify_email_link(
    token: str = Query(..., description="URL-safe verification token"),
    email: EmailStr = Query(..., description="User email address"),
) -> Dict[str, Any]:
    """Validates the email verification link clicked by the user."""
    await OTPService.verify_link_token(email, token)
    return {
        "success": True,
        "message": f"Email '{email}' has been verified successfully.",
        "email": email,
        "verified": True,
    }


@router.post("/verify-otp", status_code=status.HTTP_200_OK)
async def verify_email_otp(req: VerifyOTPRequest) -> Dict[str, Any]:
    """Validates the 6-digit verification OTP code."""
    await OTPService.verify_otp(req.email, req.otp)
    return {
        "success": True,
        "message": f"Email '{req.email}' verified successfully.",
        "verified": True,
    }
