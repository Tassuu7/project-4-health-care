"""
AegisCare Enterprise Patient Management System - User & Authentication Models
Defines accounts, role memberships, authentication state, and session tokens.
"""

from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, Enum as SQLEnum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.core.constants import UserRole
from app.db.base import Base, TimestampMixin, SoftDeleteMixin, AuditMixin


class User(Base, TimestampMixin, SoftDeleteMixin, AuditMixin):
    """User account entity storing credentials, role, and account status."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(64), unique=True, index=True, nullable=False, doc="Unique login username")
    email = Column(String(128), unique=True, index=True, nullable=False, doc="Primary email address")
    hashed_password = Column(String(255), nullable=False, doc="Bcrypt hashed password")
    role = Column(SQLEnum(UserRole), default=UserRole.PATIENT, nullable=False, index=True)
    
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64), nullable=False)
    phone_number = Column(String(32), nullable=True)
    
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    failed_login_attempts = Column(Integer, default=0, nullable=False)
    locked_until = Column(DateTime(timezone=True), nullable=True)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    doctor_profile = relationship("Doctor", back_populates="user", uselist=False)
    patient_profile = relationship("Patient", back_populates="user", uselist=False)
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")

    @property
    def full_name(self) -> str:
        """Return formatted full name."""
        return f"{self.first_name} {self.last_name}".strip()

    def is_locked(self) -> bool:
        """Determine if user account is currently locked due to failed attempts."""
        if self.locked_until and self.locked_until > datetime.now(timezone.utc):
            return True
        return False


class UserProfile(Base, TimestampMixin):
    """Extended user metadata, preferences, and avatar references."""
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    avatar_url = Column(String(255), nullable=True)
    bio = Column(Text, nullable=True)
    preferred_language = Column(String(10), default="en-US", nullable=False)
    theme_preference = Column(String(16), default="light", nullable=False)
    two_factor_enabled = Column(Boolean, default=False, nullable=False)
    two_factor_secret = Column(String(64), nullable=True)
    
    user = relationship("User", back_populates="profile")


class UserSession(Base, TimestampMixin):
    """Active user session tracking for concurrent login control and audit telemetry."""
    __tablename__ = "user_sessions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    session_token = Column(String(128), unique=True, index=True, nullable=False)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(255), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_revoked = Column(Boolean, default=False, nullable=False)

    user = relationship("User", back_populates="sessions")


class PasswordResetToken(Base, TimestampMixin):
    """Temporary cryptographic tokens for password reset verification."""
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String(128), unique=True, index=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_used = Column(Boolean, default=False, nullable=False)
