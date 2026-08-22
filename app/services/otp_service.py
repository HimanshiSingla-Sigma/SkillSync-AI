import random
import string
from datetime import datetime, timedelta, timezone
from typing import Any, Dict
from app.core.mongodb import MongoDBManager
from app.core.logging import logger
from app.services.email_service import EmailService
from app.utils.exceptions import BadRequestException


class OTPService:
    """Manages email verification OTPs and cryptographically signed verification links."""

    OTP_EXPIRY_MINUTES = 60  # 1 hour expiration window

    @classmethod
    def get_collection(cls):
        db = MongoDBManager.get_database()
        return db["email_verifications"]

    @classmethod
    def generate_otp(cls, length: int = 6) -> str:
        """Generates a secure 6-digit numeric OTP."""
        return "".join(random.choices(string.digits, k=length))

    @classmethod
    async def send_verification(cls, email: str) -> Dict[str, Any]:
        """Generates token + OTP and dispatches email directly to the recipient's Gmail inbox."""
        clean_email = email.strip().lower()
        otp = cls.generate_otp(6)
        token = EmailService.generate_verification_token()
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(minutes=cls.OTP_EXPIRY_MINUTES)

        collection = cls.get_collection()
        await collection.update_one(
            {"email": clean_email},
            {
                "$set": {
                    "email": clean_email,
                    "otp": otp,
                    "token": token,
                    "created_at": now,
                    "expires_at": expires_at,
                    "is_verified": False,
                    "attempts": 0,
                }
            },
            upsert=True,
        )

        # Dispatch email via EmailService to user's Gmail
        email_res = await EmailService.send_verification_email(clean_email, token, otp)

        return {
            "success": True,
            "message": f"Verification email dispatched to {clean_email}. Please check your Gmail inbox.",
            "sent_via_smtp": email_res.get("sent_via_smtp", False),
        }

    @classmethod
    async def verify_link_token(cls, email: str, token: str) -> bool:
        """Validates verification link token from email click."""
        clean_email = email.strip().lower()
        clean_token = token.strip()

        collection = cls.get_collection()
        record = await collection.find_one({"email": clean_email})

        if not record:
            raise BadRequestException("No verification request found for this email.")

        expires_at = record.get("expires_at")
        if isinstance(expires_at, datetime):
            if expires_at.tzinfo is None:
                expires_at = expires_at.replace(tzinfo=timezone.utc)
            if datetime.now(timezone.utc) > expires_at:
                raise BadRequestException("Verification link has expired. Please request a new verification email.")

        if record.get("token") != clean_token:
            raise BadRequestException("Invalid verification link.")

        await collection.update_one(
            {"email": clean_email},
            {"$set": {"is_verified": True, "verified_at": datetime.now(timezone.utc)}},
        )

        logger.info(f"✓ [EMAIL LINK VERIFIED] Successfully verified email '{clean_email}' via email click.")
        return True

    @classmethod
    async def verify_otp(cls, email: str, otp: str) -> bool:
        """Validates the 6-digit OTP code received in Gmail."""
        clean_email = email.strip().lower()
        clean_otp = str(otp).strip()

        collection = cls.get_collection()
        record = await collection.find_one({"email": clean_email})

        if not record:
            raise BadRequestException("No verification request found for this email. Please request a new email.")

        expires_at = record.get("expires_at")
        if isinstance(expires_at, datetime):
            if expires_at.tzinfo is None:
                expires_at = expires_at.replace(tzinfo=timezone.utc)
            if datetime.now(timezone.utc) > expires_at:
                raise BadRequestException("Verification code has expired. Please request a new email.")

        attempts = record.get("attempts", 0)
        if attempts >= 5:
            raise BadRequestException("Too many failed attempts. Please request a fresh code.")

        if record.get("otp") != clean_otp:
            await collection.update_one({"email": clean_email}, {"$inc": {"attempts": 1}})
            raise BadRequestException("Invalid verification code. Please check your Gmail inbox and try again.")

        await collection.update_one(
            {"email": clean_email},
            {"$set": {"is_verified": True, "verified_at": datetime.now(timezone.utc)}},
        )

        logger.info(f"✓ [EMAIL OTP VERIFIED] Successfully verified email '{clean_email}'.")
        return True

    @classmethod
    async def is_verified(cls, email: str) -> bool:
        """Checks if the email has been verified within the last 60 minutes."""
        clean_email = email.strip().lower()
        collection = cls.get_collection()
        record = await collection.find_one({"email": clean_email})

        if not record or not record.get("is_verified", False):
            return False

        verified_at = record.get("verified_at")
        if isinstance(verified_at, datetime):
            if verified_at.tzinfo is None:
                verified_at = verified_at.replace(tzinfo=timezone.utc)
            if datetime.now(timezone.utc) - verified_at > timedelta(minutes=60):
                return False

        return True
