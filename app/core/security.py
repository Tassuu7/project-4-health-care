import hashlib
import hmac
import os
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional, Union
import jwt
from app.config import get_settings
from app.core.exceptions import AuthenticationError

settings = get_settings()


def hash_password(password: str) -> str:
    """Hash plaintext password using PBKDF2-HMAC-SHA256 with 100,000 rounds and random salt."""
    if not password or len(password) < 6:
        raise ValueError("Password must be at least 6 characters long")
    salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    return f"pbkdf2_sha256$100000${salt.hex()}${key.hex()}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plaintext password against PBKDF2-HMAC-SHA256 hashed password."""
    if not plain_password or not hashed_password:
        return False
    try:
        if hashed_password.startswith("pbkdf2_sha256$"):
            parts = hashed_password.split("$")
            if len(parts) != 4:
                return False
            iterations = int(parts[1])
            salt = bytes.fromhex(parts[2])
            expected_key = bytes.fromhex(parts[3])
            key = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt, iterations)
            return hmac.compare_digest(key, expected_key)
        return False
    except Exception:
        return False


def create_access_token(
    subject: Union[str, int],
    role: str,
    email: str,
    full_name: str,
    expires_delta: Optional[timedelta] = None,
    extra_claims: Optional[Dict[str, Any]] = None
) -> str:
    """Generate a cryptographically signed JWT access token for authenticated session."""
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    payload = {
        "sub": str(subject),
        "role": role,
        "email": email,
        "name": full_name,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "iss": "AegisCare-Auth-Engine",
        "aud": "AegisCare-Client-Portal"
    }
    
    if extra_claims:
        payload.update(extra_claims)
        
    encoded_jwt = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(
    subject: Union[str, int],
    role: str,
    expires_delta: Optional[timedelta] = None
) -> str:
    """Generate a long-lived JWT refresh token."""
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        
    payload = {
        "sub": str(subject),
        "role": role,
        "type": "refresh",
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "iss": "AegisCare-Auth-Engine"
    }
    
    encoded_jwt = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str) -> Dict[str, Any]:
    """Decode and validate signature and expiry of JWT token."""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
            audience="AegisCare-Client-Portal",
            issuer="AegisCare-Auth-Engine"
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthenticationError("Authentication token has expired. Please log in again.")
    except jwt.InvalidTokenError:
        raise AuthenticationError("Invalid authentication token. Verification failed.")
    except Exception as e:
        raise AuthenticationError(f"Token decoding error: {str(e)}")


def decode_token_unverified(token: str) -> Dict[str, Any]:
    """Decode token claims without signature check (for debugging/header parsing)."""
    try:
        return jwt.decode(token, options={"verify_signature": False})
    except Exception:
        return {}
