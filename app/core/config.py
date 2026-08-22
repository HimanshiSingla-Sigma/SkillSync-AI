import os
from typing import List, Optional, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    PROJECT_NAME: str = "CareerConnect AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    SECRET_KEY: str = "careerconnect-ai-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "careerconnect_ai"
    MONGODB_MIN_POOL_SIZE: int = 10
    MONGODB_MAX_POOL_SIZE: int = 50

    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "password123"
    NEO4J_MAX_CONNECTION_POOL_SIZE: int = 50

    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3:latest"
    OLLAMA_EMBED_MODEL: str = "nomic-embed-text:latest"
    OLLAMA_REQUEST_TIMEOUT: float = 120.0
    GEMINI_API_KEY: Optional[str] = None

    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: str = "no-reply@careerconnect.ai"
    EMAILS_FROM_NAME: str = "CareerConnect AI"
    FRONTEND_URL: str = "http://localhost:8000"

    UPLOAD_DIR: str = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../uploads/resumes")
    )
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_EXTENSIONS: List[str] = ["pdf", "docx"]

    CORS_ORIGINS: List[str] = ["*"]

    @field_validator("UPLOAD_DIR", mode="before")
    @classmethod
    def assemble_upload_dir(cls, v: Union[str, None]) -> str:
        default_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../uploads/resumes")
        )
        if not v or v.startswith("/app/"):
            return default_dir
        if not os.path.isabs(v):
            return os.path.abspath(
                os.path.join(os.path.dirname(__file__), "../../", v)
            )
        return v

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        return ["*"]


settings = Settings()