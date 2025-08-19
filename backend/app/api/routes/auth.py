"""
app/api/routes/auth.py

Auth endpoints:
- POST /auth/login
- POST /auth/refresh
- POST /auth/change-password
- POST /auth/logout (refresh invalidation via version bump)
"""
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
import jwt

from app.core.auth import get_current_user
from app.core.rbac import Role
from app.core.security import verify_password, hash_password, create_access_token, create_refresh_token, decode_token
from app.core.config import settings
from app.db.session import get_db
from app.crud.user import users as users_crud
from app.schemas.auth import LoginRequest, TokenPair, RefreshRequest, ChangePasswordRequest
from app.services.phone import normalize_phone

router = APIRouter(prefix="/auth", tags=["auth"])


def _scope_for(user):
    if user.role == Role.REGIONAL_MANAGER and user.regional_manager_profile:
        return {"region_id": str(user.regional_manager_profile.region_id)}
    if user.role in (Role.BRANCH_MANAGER, Role.PATIENT):
        prof = user.branch_manager_profile if user.role == Role.BRANCH_MANAGER else user.patient_profile
        if prof:
            return {"branch_id": str(prof.branch_id)}
    return {}


@router.post("/login", response_model=TokenPair)
def login(body: LoginRequest, request: Request, db: Session = Depends(get_db)):
    phone = normalize_phone(body.phone)
    user = users_crud.get_by_phone(db, phone)
    if not user or not user.is_active or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid phone or password")

    # issue tokens
    access = create_access_token(sub=str(user.id), role=user.role.value, scope=_scope_for(user))
    refresh = create_refresh_token(sub=str(user.id), role=user.role.value, rtv=user.refresh_token_version)

    # update last login (no secrets stored)
    user.last_login_at = None  # Optional: set to datetime.utcnow() if desired.
    db.add(user)
    db.flush()

    return TokenPair(access_token=access, refresh_token=refresh, must_change_password=user.must_change_password)


@router.post("/refresh", response_model=TokenPair)
def refresh_tokens(body: RefreshRequest, db: Session = Depends(get_db)):
    try:
        payload = decode_token(body.refresh_token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh expired")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")

    user = users_crud.get_by_id(db, payload.get("sub"))
    if not user or not user.is_active:
        raise HTTPException(status_code=403, detail="User inactive")

    if int(payload.get("rtv", -1)) != int(user.refresh_token_version):
        raise HTTPException(status_code=401, detail="Stale refresh token")

    # rotate
    users_crud.increment_rtv(db, user)
    access = create_access_token(sub=str(user.id), role=user.role.value, scope=_scope_for(user))
    refresh = create_refresh_token(sub=str(user.id), role=user.role.value, rtv=user.refresh_token_version)
    return TokenPair(access_token=access, refresh_token=refresh, must_change_password=user.must_change_password)


@router.post("/change-password")
def change_password(body: ChangePasswordRequest, user=Depends(get_current_user), db: Session = Depends(get_db)):
    if not user.must_change_password:
        # Verify current password
        if not body.current_password:
            raise HTTPException(status_code=400, detail="current_password required")
        if not verify_password(body.current_password, user.password_hash):
            raise HTTPException(status_code=400, detail="Invalid current_password")

    new_hash = hash_password(body.new_password)
    users_crud.set_password(db, user, new_hash)
    # Invalidate existing refresh by bumping version
    users_crud.increment_rtv(db, user)
    return {"message": "Password updated"}


@router.post("/logout")
def logout(user=Depends(get_current_user), db: Session = Depends(get_db)):
    # Invalidate refresh token by version bump; access token will naturally expire.
    users_crud.increment_rtv(db, user)
    return {"message": "Logged out"}
