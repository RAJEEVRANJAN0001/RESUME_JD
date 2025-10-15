"""
Configuration module for Smart Resume Screener.
Loads environment variables and provides application settings.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Gemini AI
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.0-flash"  # Updated to latest available model
    
    # Azure Document Intelligence
    AZURE_DOC_INTELLIGENCE_ENDPOINT: str
    AZURE_DOC_INTELLIGENCE_KEY: str
    
    # MongoDB
    MONGODB_URI: str
    DATABASE_NAME: str = "resume_screener"
    
    # JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 1440
    
    # Application
    ENVIRONMENT: str = "development"
    API_VERSION: str = "v1"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
