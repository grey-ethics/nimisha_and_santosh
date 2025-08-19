"""
app/api/routes/patients.py

Patient-facing endpoints:
- GET /me
- (Placeholders) GET /education, /shop, /orders
"""
from fastapi import APIRouter, Depends
from app.core.auth import role_required
from app.core.rbac import Role
from app.schemas.user import UserOut

router = APIRouter(prefix="/me", tags=["patients"], dependencies=[Depends(role_required(Role.PATIENT))])


@router.get("", response_model=UserOut)
def me(user=Depends(role_required(Role.PATIENT))):
    return user


# Placeholders
extra_router = APIRouter(prefix="/patient", tags=["placeholders"], dependencies=[Depends(role_required(Role.PATIENT))])

@extra_router.get("/education")
def education():
    return []

@extra_router.get("/shop")
def shop():
    return []

@extra_router.get("/orders")
def orders():
    return []
