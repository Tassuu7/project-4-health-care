"""
AegisCare Enterprise Patient Management System - Authentication Service
Handles login validation, JWT tokens, password hashing, and role checks.
"""

from datetime import datetime, timezone
from typing import Any, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from app.core.constants import AuditAction, UserRole
from app.core.exceptions import AuthenticationError, ResourceConflictError, ValidationError
from app.core.security import create_access_token, create_refresh_token, hash_password, verify_password
from app.models.user import User, UserProfile
from app.repositories.audit_repo import AuditRepository
from app.repositories.user_repo import UserRepository
from app.schemas.user import UserCreate, UserLogin, UserResponse


class AuthService:
    """Business logic for user authentication, registration, and session security."""

    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.audit_repo = AuditRepository(db)

    def authenticate_user(self, login_data: UserLogin, ip_address: Optional[str] = None) -> Tuple[User, str, str]:
        """Authenticate user credentials, enforce lockout rules, and generate JWT tokens."""
        user = self.user_repo.get_by_username_or_email(login_data.username_or_email)
        if not user:
            self.audit_repo.log_event(
                action=AuditAction.LOGIN_FAILURE,
                resource_type="AUTH",
                username=login_data.username_or_email,
                ip_address=ip_address,
                details="User not found"
            )
            raise AuthenticationError("Invalid username or password")

        if user.is_locked():
            raise AuthenticationError("Account is temporarily locked due to multiple failed login attempts.")

        if not verify_password(login_data.password, user.hashed_password):
            user.failed_login_attempts += 1
            self.db.commit()
            self.audit_repo.log_event(
                action=AuditAction.LOGIN_FAILURE,
                resource_type="AUTH",
                user_id=user.id,
                username=user.username,
                user_role=user.role.value,
                ip_address=ip_address,
                details=f"Incorrect password attempt {user.failed_login_attempts}"
            )
            raise AuthenticationError("Invalid username or password")

        # Reset failed attempts on success
        user.failed_login_attempts = 0
        user.last_login_at = datetime.now(timezone.utc)
        self.db.commit()

        access_token = create_access_token(
            subject=user.id,
            role=user.role.value,
            email=user.email,
            full_name=user.full_name
        )
        refresh_token = create_refresh_token(subject=user.id, role=user.role.value)

        self.audit_repo.log_event(
            action=AuditAction.LOGIN_SUCCESS,
            resource_type="AUTH",
            user_id=user.id,
            username=user.username,
            user_role=user.role.value,
            ip_address=ip_address,
            details="User logged in successfully"
        )
        return user, access_token, refresh_token

    def register_user(self, user_in: UserCreate, ip_address: Optional[str] = None) -> User:
        """Register a new user account with hashed password and default profile."""
        if self.user_repo.get_by_username(user_in.username):
            raise ResourceConflictError(f"Username '{user_in.username}' is already registered.")
        if self.user_repo.get_by_email(user_in.email):
            raise ResourceConflictError(f"Email '{user_in.email}' is already registered.")

        new_user = User(
            username=user_in.username.strip().lower(),
            email=user_in.email.strip().lower(),
            hashed_password=hash_password(user_in.password),
            role=user_in.role,
            first_name=user_in.first_name.strip(),
            last_name=user_in.last_name.strip(),
            phone_number=user_in.phone_number,
            is_active=True,
            is_verified=True
        )
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)

        profile = UserProfile(user_id=new_user.id)
        self.db.add(profile)
        self.db.commit()

        return new_user
