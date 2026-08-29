"""
AegisCare Enterprise Patient Management System - User Repository
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.constants import UserRole
from app.models.user import User, UserSession
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Data access repository for User accounts and authentication sessions."""

    def __init__(self, db: Session):
        super().__init__(User, db)

    def get_by_username(self, username: str) -> Optional[User]:
        """Find active user by username."""
        return self.db.query(User).filter(
            User.username == username.strip().lower(),
            User.is_deleted == False
        ).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """Find active user by email."""
        return self.db.query(User).filter(
            User.email == email.strip().lower(),
            User.is_deleted == False
        ).first()

    def get_by_username_or_email(self, identifier: str) -> Optional[User]:
        """Lookup user by either username or email address."""
        identifier = identifier.strip().lower()
        return self.db.query(User).filter(
            (User.username == identifier) | (User.email == identifier),
            User.is_deleted == False
        ).first()

    def list_by_role(self, role: UserRole) -> List[User]:
        """List all active users belonging to a specific role."""
        return self.db.query(User).filter(
            User.role == role,
            User.is_active == True,
            User.is_deleted == False
        ).all()
