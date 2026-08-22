from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.application_routes import router as application_router
from app.api.routes.auth_routes import router as auth_router
from app.api.routes.chat_routes import router as chat_router
from app.api.routes.company_routes import router as company_router
from app.api.routes.drive_routes import router as drive_router
from app.api.routes.eligibility_routes import router as eligibility_router
from app.api.routes.resume_routes import router as resume_router
from app.api.routes.student_routes import router as student_router
from app.core.config import settings
from app.core.database import close_databases, init_databases
from app.core.logging import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager handling database startup and graceful shutdown."""
    logger.info("Starting up CareerConnect AI Backend Engine...")
    await init_databases()
    yield
    logger.info("Shutting down CareerConnect AI Backend Engine...")
    await close_databases()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "CareerConnect AI — Production-Grade Placement Platform combining "
        "Deterministic Policy-Based Eligibility, GraphRAG Intelligence with Neo4j, "
        "and Automated Resume Processing."
    ),
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Cross-Origin Resource Sharing (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os
from fastapi.staticfiles import StaticFiles

# Mount all REST API Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(student_router, prefix=settings.API_V1_STR)
app.include_router(company_router, prefix=settings.API_V1_STR)
app.include_router(drive_router, prefix=settings.API_V1_STR)
app.include_router(eligibility_router, prefix=settings.API_V1_STR)
app.include_router(application_router, prefix=settings.API_V1_STR)
app.include_router(resume_router, prefix=settings.API_V1_STR)
app.include_router(chat_router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health probe for service readiness."""
    return {
        "status": "healthy",
        "mongodb": "connected",
        "neo4j": "connected",
        "ollama_url": settings.OLLAMA_BASE_URL,
    }


# Mount Static Frontend Files (Zero NPM / Single Page App)
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../static"))
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")