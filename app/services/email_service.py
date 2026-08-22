import os
import secrets
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Dict, Optional
from dotenv import load_dotenv
from app.core.config import settings
from app.core.logging import logger


class EmailService:
    """Handles transactional verification email dispatches via Gmail / SMTP."""

    @classmethod
    def get_smtp_config(cls) -> Dict[str, Any]:
        """Dynamically loads SMTP credentials from .env and settings."""
        load_dotenv(override=True)
        smtp_host = os.getenv("SMTP_HOST", settings.SMTP_HOST or "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", settings.SMTP_PORT or 587))
        smtp_user = os.getenv("SMTP_USER", settings.SMTP_USER or "").strip()
        smtp_password = os.getenv("SMTP_PASSWORD", settings.SMTP_PASSWORD or "").strip()
        emails_from = os.getenv("EMAILS_FROM_EMAIL", settings.EMAILS_FROM_EMAIL or smtp_user).strip()
        emails_name = os.getenv("EMAILS_FROM_NAME", settings.EMAILS_FROM_NAME or "CareerConnect AI").strip()
        frontend_url = os.getenv("FRONTEND_URL", settings.FRONTEND_URL or "http://localhost:8000").rstrip("/")

        return {
            "host": smtp_host,
            "port": smtp_port,
            "user": smtp_user,
            "password": smtp_password,
            "from_email": emails_from or smtp_user,
            "from_name": emails_name,
            "frontend_url": frontend_url,
        }

    @classmethod
    def generate_verification_token(cls) -> str:
        """Generates a cryptographically secure URL-safe verification token."""
        return secrets.token_urlsafe(32)

    @classmethod
    def get_verification_url(cls, email: str, token: str) -> str:
        """Constructs the frontend email verification confirmation URL."""
        config = cls.get_smtp_config()
        return f"{config['frontend_url']}/?action=verify_email&token={token}&email={email}"

    @classmethod
    def create_html_email(cls, recipient_email: str, verification_url: str, otp: str) -> str:
        """Generates a high-end HTML email with verification button and OTP code."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #0b0f19; color: #f1f5f9; margin: 0; padding: 20px; }}
            .container {{ max-width: 580px; margin: 0 auto; background: #111827; border-radius: 20px; border: 1px solid #1f2937; overflow: hidden; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7); }}
            .header {{ background: linear-gradient(135deg, #4f46e5, #7c3aed); padding: 35px 24px; text-align: center; }}
            .header h1 {{ margin: 0; color: #ffffff; font-size: 24px; font-weight: 800; letter-spacing: -0.5px; }}
            .header p {{ margin: 6px 0 0 0; color: #e0e7ff; font-size: 13px; font-weight: 500; }}
            .body {{ padding: 35px 30px; line-height: 1.6; color: #cbd5e1; font-size: 15px; }}
            .highlight {{ color: #a5b4fc; font-weight: 700; }}
            .btn-container {{ text-align: center; margin: 28px 0; }}
            .btn {{ display: inline-block; background: linear-gradient(135deg, #6366f1, #8b5cf6); color: #ffffff !important; padding: 14px 36px; border-radius: 12px; font-weight: 700; text-decoration: none; font-size: 15px; box-shadow: 0 10px 25px rgba(99, 102, 241, 0.4); }}
            .otp-box {{ background: #1e293b; border: 1px solid #334155; border-radius: 14px; padding: 18px; text-align: center; margin: 24px 0; }}
            .otp-label {{ font-size: 11px; text-transform: uppercase; letter-spacing: 1.5px; color: #94a3b8; margin-bottom: 6px; }}
            .otp-digits {{ font-size: 32px; font-weight: 900; letter-spacing: 6px; color: #38bdf8; font-family: monospace; }}
            .footer {{ border-top: 1px solid #1f2937; padding: 20px 30px; font-size: 12px; color: #64748b; text-align: center; background: #0b0f19; }}
            .link-box {{ word-break: break-all; background: #0b0f19; padding: 12px; border-radius: 8px; border: 1px solid #1f2937; font-family: monospace; font-size: 12px; color: #94a3b8; margin-top: 12px; }}
          </style>
        </head>
        <body>
          <div class="container">
            <div class="header">
              <h1>CareerConnect AI</h1>
              <p>Autonomous Placement & Knowledge Graph Platform</p>
            </div>
            <div class="body">
              <p>Hello,</p>
              <p>Welcome to <strong>CareerConnect AI</strong>. To activate your account and verify your email address (<span class="highlight">{recipient_email}</span>), please click the button below:</p>
              
              <div class="btn-container">
                <a href="{verification_url}" class="btn" target="_blank">Verify Email Address</a>
              </div>

              <div class="otp-box">
                <div class="otp-label">Or use your 6-digit verification code</div>
                <div class="otp-digits">{otp}</div>
              </div>
              
              <p style="font-size: 13px; color: #94a3b8;">This verification email will remain active for <strong>60 minutes</strong>.</p>
              
              <p style="font-size: 12px; margin-bottom: 5px; color: #64748b;">Direct Verification Link:</p>
              <div class="link-box">{verification_url}</div>
            </div>
            <div class="footer">
              &copy; 2026 CareerConnect AI. Deterministic Placement & Knowledge Graph Intelligence.
            </div>
          </div>
        </body>
        </html>
        """

    @classmethod
    async def send_verification_email(cls, recipient_email: str, token: str, otp: str) -> Dict[str, Any]:
        """Dispatches verification email via Gmail / SMTP with real-time config loading."""
        clean_email = recipient_email.strip().lower()
        cfg = cls.get_smtp_config()
        verification_url = cls.get_verification_url(clean_email, token)

        logger.info(
            f"\n"
            f"===============================================================\n"
            f"📧 [DISPATCHING GMAIL VERIFICATION]\n"
            f"To: {clean_email}\n"
            f"Sender: {cfg['user']}\n"
            f"OTP Code: {otp}\n"
            f"Link: {verification_url}\n"
            f"==============================================================="
        )

        sent_via_smtp = False
        smtp_error = None

        if cfg["host"] and cfg["user"] and cfg["password"]:
            try:
                msg = MIMEMultipart("alternative")
                msg["Subject"] = "Verify your email for CareerConnect AI"
                from_email = cfg["from_email"] or cfg["user"]
                from_name = cfg["from_name"] or "CareerConnect AI"
                msg["From"] = f"{from_name} <{from_email}>"
                msg["To"] = clean_email

                html_content = cls.create_html_email(clean_email, verification_url, otp)
                msg.attach(MIMEText(html_content, "html"))

                if cfg["port"] == 465:
                    with smtplib.SMTP_SSL(cfg["host"], cfg["port"], timeout=15) as server:
                        server.login(cfg["user"], cfg["password"])
                        server.sendmail(from_email, [clean_email], msg.as_string())
                else:
                    with smtplib.SMTP(cfg["host"], cfg["port"], timeout=15) as server:
                        server.starttls()
                        server.login(cfg["user"], cfg["password"])
                        server.sendmail(from_email, [clean_email], msg.as_string())

                sent_via_smtp = True
                logger.info(f"✓ Real email successfully delivered to Gmail '{clean_email}' via SMTP ({cfg['host']}).")
            except Exception as e:
                smtp_error = str(e)
                logger.error(f"❌ Failed to send email to Gmail ({e}).")

        return {
            "success": True,
            "message": f"Verification email dispatched to {clean_email}.",
            "sent_via_smtp": sent_via_smtp,
            "smtp_error": smtp_error,
            "verification_url": verification_url,
        }
