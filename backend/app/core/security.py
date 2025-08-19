"""
app/core/security.py

Security primitives:
- Password hashing via passlib (bcrypt).
- JWT encode/decode (access & refresh).
- Token versioning for refresh rotation.
"""
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import jwt
from passlib.hash import bcrypt

from app.core.config import settings


def hash_password(plain: str) -> str:
    return bcrypt.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.verify(plain, hashed)
    except Exception:
        return False


def _dt(exp_in_seconds: int) -> datetime:
    return datetime.now(tz=timezone.utc) + timedelta(seconds=exp_in_seconds)


def create_access_token(sub: str, role: str, scope: Dict[str, Any] | None = None) -> str:
    expire = _dt(settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    to_encode = {
        "sub": sub,
        "role": role,
        "scope": scope or {},
        "type": "access",
        "exp": int(expire.timestamp()),
        "iat": int(datetime.now(tz=timezone.utc).timestamp()),
    }
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(sub: str, role: str, rtv: int) -> str:
    expire = _dt(settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 3600)
    to_encode = {
        "sub": sub,
        "role": role,
        "rtv": rtv,  # refresh token version (per-user rotation)
        "type": "refresh",
        "exp": int(expire.timestamp()),
        "iat": int(datetime.now(tz=timezone.utc).timestamp()),
    }
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
