"""
Unit Tests for Authentication, Password Hashing, and JWT Token Security
"""

import pytest
from app.core.security import create_access_token, decode_token, hash_password, verify_password
from app.models.user import User
from app.core.constants import UserRole
from app.services.auth_service import AuthService
from app.schemas.user import UserCreate, UserLogin


def test_password_hashing():
    """Test bcrypt hashing and verification."""
    raw = "Doctor@123"
    hashed = hash_password(raw)
    assert hashed != raw
    assert verify_password(raw, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_jwt_token_creation_and_decoding():
    """Test JWT access token issuance and claims verification."""
    token = create_access_token(subject=1, role="DOCTOR", email="dr.smith@example.com", full_name="Dr. Smith")
    assert isinstance(token, str)
    claims = decode_token(token)
    assert claims["sub"] == "1"
    assert claims["role"] == "DOCTOR"
    assert claims["name"] == "Dr. Smith"


def test_user_registration_and_login(db_session):
    """Test full user registration and authentication workflow."""
    service = AuthService(db_session)
    user_in = UserCreate(
        username="dr.watson",
        email="dr.watson@example.com",
        password="WatsonPassword123",
        role=UserRole.DOCTOR,
        first_name="John",
        last_name="Watson"
    )
    user = service.register_user(user_in)
    assert user.id is not None
    assert user.username == "dr.watson"

    # Authenticate
    auth_user, access_token, _ = service.authenticate_user(
        UserLogin(username_or_email="dr.watson", password="WatsonPassword123")
    )
    assert auth_user.id == user.id
    assert access_token is not None
