"""
app/core/auth.py

Auth dependencies:
- get_current_user: validates JWT, active, and must_change_password (except auth endpoints).
- role_required: decorator-like dependency for role checks.
- scope checks for region/branch operations.
"""
from typing import Optional
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
import jwt

from app.core.security import decode_token
from app.core.rbac import Role
from app.db.session import get_db
from app.crud.user import users as users_crud

bearer = HTTPBearer(auto_error=False)

AUTH_WHITELIST_PATHS = {"/auth/login", "/auth/refresh", "/auth/logout", "/docs", "/openapi.json", "/redoc"}


def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
    creds: Optional[HTTPAuthorizationCredentials] = Depends(bearer),
):
    if not creds or not creds.scheme.lower() == "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        payload = decode_token(creds.credentials)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Use access token")

    user_id = payload.get("sub")
    user = users_crud.get_by_id(db, user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive or missing user")

    # Enforce must_change_password everywhere except whitelisted endpoints.
    if user.must_change_password and request.url.path not in AUTH_WHITELIST_PATHS and request.url.path != "/auth/change-password":
        raise HTTPException(status_code=403, detail="Password change required")

    return user


def role_required(*allowed: Role):
    def _dep(user=Depends(get_current_user)):
        if user.role not in allowed:
            raise HTTPException(status_code=403, detail="Insufficient role")
        return user
    return _dep


def require_scope_region(region_id: str, user=Depends(get_current_user)):
    """RM scope guard: user must be RM for region, or Admin."""
    if user.role == Role.ADMIN:
        return user
    if user.role == Role.REGIONAL_MANAGER:
        if user.regional_manager_profile and str(user.regional_manager_profile.region_id) == str(region_id):
            return user
    raise HTTPException(status_code=403, detail="Region scope denied")


def require_scope_branch(branch_id: str, user=Depends(get_current_user)):
    """BM/Patient branch guard: user must be BM/Patient of branch, or Admin/RM (if branch in their region)."""
    if user.role == Role.ADMIN:
        return user
    if user.role == Role.BRANCH_MANAGER and user.branch_manager_profile and str(user.branch_manager_profile.branch_id) == str(branch_id):
        return user
    if user.role == Role.PATIENT and user.patient_profile and str(user.patient_profile.branch_id) == str(branch_id):
        return user
    # RM may view within their region; write ops will use explicit RM-only checks in routers.
    if user.role == Role.REGIONAL_MANAGER and user.regional_manager_profile:
        # Check branch belongs to their region at router level; here we allow and routers confirm.
        return user
    raise HTTPException(status_code=403, detail="Branch scope denied")
