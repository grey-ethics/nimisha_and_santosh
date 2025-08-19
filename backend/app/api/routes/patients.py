"""
app/api/routes/patients.py

Endpoints:
- GET /me: return the current authenticated user (any role)
- Patient placeholders (/patient/*): patient-only
"""
from fastapi import APIRouter, Depends

from app.core.auth import get_current_user, role_required
from app.core.rbac import Role
from app.schemas.user import UserOut

# ---- Generic /me (works for ADMIN, REGIONAL_MANAGER, BRANCH_MANAGER, PATIENT) ----
router = APIRouter(prefix="/me", tags=["patients"])  # keep tag to match existing OpenAPI

@router.get("", response_model=UserOut)
def me(user=Depends(get_current_user)):
    return user


# ---- Patient-only placeholders remain restricted to PATIENT ----
extra_router = APIRouter(
    prefix="/patient",
    tags=["placeholders"],
    dependencies=[Depends(role_required(Role.PATIENT))],
)

@extra_router.get("/education")
def education():
    return []

@extra_router.get("/shop")
def shop():
    return []

@extra_router.get("/orders")
def orders():
    return []
