"""
FastAPI main application entry point.
Smart Resume Screener API.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import connect_to_mongo, close_mongo_connection
from app.routers import auth, resumes, upload, analytics, settings
from app.config import settings as config_settings
from app.icons import ROCKET, CHECK_MARK

# Create FastAPI application
app = FastAPI(
    title="Smart Resume Screener API",
    description="Intelligent resume parsing and screening using Azure AI and Google Gemini",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup."""
    print(f"{ROCKET} Starting Smart Resume Screener API...")
    await connect_to_mongo()
    print(f"{CHECK_MARK} Environment: {config_settings.ENVIRONMENT}")
    print(f"{CHECK_MARK} API Version: {config_settings.API_VERSION}")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection on shutdown."""
    print("🛑 Shutting down...")
    await close_mongo_connection()

# Include routers
app.include_router(auth.router)
app.include_router(settings.router)
app.include_router(upload.router)
app.include_router(resumes.router)
app.include_router(analytics.router)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "name": "Smart Resume Screener API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "environment": settings.ENVIRONMENT
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT
    }
