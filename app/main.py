"""
AegisCare Enterprise Patient Management System - FastAPI Application Bootstrap
Mounts static assets, templates, middleware, API v1 routes, and web controllers.
"""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.v1.api_router import api_router
from app.config import get_settings
from app.core.middleware import RequestTimingMiddleware, SecurityHeadersMiddleware
from app.db.seed import seed_database
from app.db.session import init_db
from app.web.routes import web_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown event lifecycle manager."""
    # Ensure directories exist
    os.makedirs(settings.STATIC_DIR, exist_ok=True)
    os.makedirs(settings.TEMPLATES_DIR, exist_ok=True)
    os.makedirs(settings.STORAGE_DIR, exist_ok=True)
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    os.makedirs(settings.LOG_DIR, exist_ok=True)
    
    # Initialize DB & Seed Demo Data
    init_db()
    seed_database()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Enterprise Clinical & Patient Management Platform adhering to HIPAA standards.",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    lifespan=lifespan
)

# Attach Security and Timing Middlewares
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RequestTimingMiddleware)

# CORS Policy
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# Static Files Mount
if os.path.exists("app/static"):
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include Routers
app.include_router(web_router)
app.include_router(api_router, prefix=settings.API_V1_PREFIX)
