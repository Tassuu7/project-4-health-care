"""
AegisCare Enterprise Patient Management System - Authentication API Router
"""

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.core.exceptions import AuthenticationError, ResourceConflictError
from app.db.session import get_db
from app.schemas.common import ResponseEnvelope
from app.schemas.user import TokenResponse, UserCreate, UserLogin, UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=ResponseEnvelope[TokenResponse])
def login(login_data: UserLogin, request: Request, db: Session = Depends(get_db)):
    """Authenticate user with username/email and password, returning JWT access token."""
    service = AuthService(db)
    client_ip = request.client.host if request.client else "127.0.0.1"
    try:
        user, access_token, refresh_token = service.authenticate_user(login_data, ip_address=client_ip)
        user_resp = UserResponse.model_validate(user)
        token_data = TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=28800,
            user=user_resp
        )
        return ResponseEnvelope(data=token_data, message="Authentication successful")
    except AuthenticationError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.message)


@router.post("/register", response_model=ResponseEnvelope[UserResponse], status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, request: Request, db: Session = Depends(get_db)):
    """Register a new patient or staff user profile."""
    service = AuthService(db)
    client_ip = request.client.host if request.client else "127.0.0.1"
    try:
        user = service.register_user(user_in, ip_address=client_ip)
        return ResponseEnvelope(data=UserResponse.model_validate(user), message="Account registered successfully")
    except ResourceConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)
