"""
AegisCare Enterprise Patient Management System - Configuration Module
Provides strongly-typed configuration settings with validation and environment loading.
"""

import os
from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings schema and configuration manager."""
    
    # Application Metadata
    APP_NAME: str = Field(default="AegisCare Enterprise Patient Management Platform")
    APP_VERSION: str = Field(default="4.2.0")
    APP_ENV: str = Field(default="development")
    APP_DEBUG: bool = Field(default=True)
    APP_HOST: str = Field(default="0.0.0.0")
    APP_PORT: int = Field(default=8000)
    APP_URL: str = Field(default="http://localhost:8000")
    API_V1_PREFIX: str = Field(default="/api/v1")
    
    # Security and Secret Keys
    SECRET_KEY: str = Field(default="aegiscare_enterprise_super_secret_master_key_change_in_production_2026")
    JWT_ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=480)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7)
    PASSWORD_HASH_ROUNDS: int = Field(default=12)
    
    # Database Configuration
    DATABASE_URL: str = Field(default="sqlite:///./aegiscare_health.db")
    DB_ECHO_SQL: bool = Field(default=False)
    DB_POOL_SIZE: int = Field(default=20)
    DB_MAX_OVERFLOW: int = Field(default=10)
    DB_POOL_TIMEOUT: int = Field(default=30)
    
    # Healthcare Compliance & Security Mandates
    HIPAA_AUDIT_ENABLED: bool = Field(default=True)
    DATA_MASKING_ENABLED: bool = Field(default=True)
    SESSION_TIMEOUT_MINUTES: int = Field(default=30)
    MAX_LOGIN_ATTEMPTS: int = Field(default=5)
    LOCKOUT_DURATION_MINUTES: int = Field(default=15)
    ENFORCE_PASSWORD_COMPLEXITY: bool = Field(default=True)
    
    # Clinical Decision Support Engine
    ENABLE_AI_TRIAGE_ASSIST: bool = Field(default=False)
    DEFAULT_TRIAGE_PROTOCOL: str = Field(default="ESI_V4")
    ENABLE_DRUG_INTERACTION_CHECK: bool = Field(default=True)
    ENABLE_CRITICAL_LAB_ALERTS: bool = Field(default=True)
    AUTO_ASSIGN_TRIAGE_ROOM: bool = Field(default=True)
    SEPSIS_EARLY_WARNING_THRESHOLD: float = Field(default=2.0)
    
    # Telehealth and Queue Engine
    MAX_QUEUE_PER_DOCTOR: int = Field(default=50)
    DEFAULT_APPOINTMENT_DURATION_MIN: int = Field(default=30)
    EMERGENCY_RESERVATION_RATIO: float = Field(default=0.15)
    
    # Notification & Messaging
    NOTIFICATION_DRIVER: str = Field(default="in_memory")
    SMTP_HOST: str = Field(default="localhost")
    SMTP_PORT: int = Field(default=1025)
    SMTP_USER: Optional[str] = Field(default=None)
    SMTP_PASS: Optional[str] = Field(default=None)
    FROM_EMAIL: str = Field(default="notifications@aegiscarehealth.local")
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = Field(default=["*"])
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True)
    CORS_ALLOW_METHODS: List[str] = Field(default=["*"])
    CORS_ALLOW_HEADERS: List[str] = Field(default=["*"])
    
    # File Storage Paths
    STATIC_DIR: str = Field(default="app/static")
    TEMPLATES_DIR: str = Field(default="app/templates")
    STORAGE_DIR: str = Field(default="storage")
    UPLOAD_DIR: str = Field(default="storage/uploads")
    LOG_DIR: str = Field(default="storage/logs")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    def is_production(self) -> bool:
        """Check if application is running in production mode."""
        return self.APP_ENV.lower() in ("production", "prod")

    def is_development(self) -> bool:
        """Check if application is running in development mode."""
        return self.APP_ENV.lower() in ("development", "dev", "local")


# Singleton instance cached across runtime
_settings_instance: Optional[Settings] = None

def get_settings() -> Settings:
    """Retrieve global settings singleton."""
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
    return _settings_instance
