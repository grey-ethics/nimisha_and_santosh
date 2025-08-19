"""
app/api/routes/admins.py

Admin endpoints:
- POST /regions, GET /regions
- POST /branches, GET /branches?region_id=...
- RM lifecycle: create/list/patch/deactivate
"""
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session

from app.core.auth import role_required
from app.core.rbac import Role
from app.db.session import get_db
from app.schemas.region import RegionCreate, RegionOut
from app.schemas.branch import BranchCreate, BranchOut
from app.schemas.user import UserOut
from app.crud.region import regions as regions_crud
from app.crud.branch import branches as branches_crud
from app.crud.user import users as users_crud
from app.models.regional_manager_profile import RegionalManagerProfile
from app.core.security import hash_password
from app.services.phone import normalize_phone
from app.services.audit import build_diff
from app.crud.audit import audits as audits_crud

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(role_required(Role.ADMIN))])


@router.post("/regions", response_model=RegionOut)
def create_region(body: RegionCreate, request: Request, db: Session = Depends(get_db), admin=Depends(role_required(Role.ADMIN))):
    region = regions_crud.create(db, body.name)
    audits_crud.log(db, actor_user_id=str(admin.id), action="CREATE", entity_type="Region", entity_id=str(region.id), diff_json=build_diff(None, region), ip=request.client.host if request.client else None)
    return region


@router.get("/regions", response_model=list[RegionOut])
def list_regions(db: Session = Depends(get_db)):
    return regions_crud.list(db)


@router.post("/branches", response_model=BranchOut)
def create_branch(body: BranchCreate, request: Request, db: Session = Depends(get_db), admin=Depends(role_required(Role.ADMIN))):
    region = regions_crud.get(db, body.region_id)
    if not region or not region.is_active:
        raise HTTPException(status_code=400, detail="Invalid region")
    branch = branches_crud.create(db, region_id=str(region.id), name=body.name, address=body.address)
    audits_crud.log(db, actor_user_id=str(admin.id), action="CREATE", entity_type="Branch", entity_id=str(branch.id), diff_json=build_diff(None, branch), ip=request.client.host if request.client else None)
    return branch


@router.get("/branches", response_model=list[BranchOut])
def list_branches(region_id: str = Query(...), db: Session = Depends(get_db)):
    return branches_crud.list_by_region(db, region_id)


# --- Regional Managers lifecycle ---

class RMCreateIn(RegionCreate.__class__):
    pass

from pydantic import BaseModel

class RegionalManagerCreate(BaseModel):
    phone: str
    password: str
    full_name: str | None = None
    email: str | None = None
    region_id: str
    notes: str | None = None


class RegionalManagerPatch(BaseModel):
    full_name: str | None = None
    email: str | None = None
    region_id: str | None = None
    notes: str | None = None


@router.post("/users/regional-managers", response_model=UserOut)
def create_rm(body: RegionalManagerCreate, request: Request, db: Session = Depends(get_db), admin=Depends(role_required(Role.ADMIN))):
    region = regions_crud.get(db, body.region_id)
    if not region or not region.is_active:
        raise HTTPException(status_code=400, detail="Invalid region")

    phone = normalize_phone(body.phone)
    if users_crud.get_by_phone(db, phone):
        raise HTTPException(status_code=400, detail="Phone already exists")

    user = users_crud.create(db, phone=phone, password_hash=hash_password(body.password), role=Role.REGIONAL_MANAGER, full_name=body.full_name, email=body.email)
    prof = RegionalManagerProfile(user_id=user.id, region_id=region.id, notes=body.notes)
    db.add(prof)
    db.flush()
    audits_crud.log(db, actor_user_id=str(admin.id), action="CREATE", entity_type="RegionalManager", entity_id=str(user.id), diff_json=build_diff(None, user), ip=request.client.host if request.client else None)
    return user


@router.get("/users/regional-managers", response_model=list[UserOut])
def list_rms(db: Session = Depends(get_db)):
    return users_crud.list_by_role(db, Role.REGIONAL_MANAGER)


@router.patch("/users/regional-managers/{user_id}", response_model=UserOut)
def patch_rm(user_id: str, body: RegionalManagerPatch, request: Request, db: Session = Depends(get_db), admin=Depends(role_required(Role.ADMIN))):
    user = users_crud.get_by_id(db, user_id)
    if not user or user.role != Role.REGIONAL_MANAGER:
        raise HTTPException(status_code=404, detail="RM not found")

    before = user.__class__(**{k: getattr(user, k) for k in user.__mapper__.attrs.keys()})  # shallow copy for diff
    if body.full_name is not None:
        user.full_name = body.full_name
    if body.email is not None:
        user.email = body.email
    if body.region_id is not None:
        user.regional_manager_profile.region_id = body.region_id
    if body.notes is not None:
        user.regional_manager_profile.notes = body.notes

    db.add(user)
    db.flush()
    audits_crud.log(db, actor_user_id=str(admin.id), action="UPDATE", entity_type="RegionalManager", entity_id=str(user.id), diff_json=build_diff(before, user), ip=request.client.host if request.client else None)
    return user


@router.post("/users/regional-managers/{user_id}:deactivate")
def deactivate_rm(user_id: str, request: Request, db: Session = Depends(get_db), admin=Depends(role_required(Role.ADMIN))):
    user = users_crud.get_by_id(db, user_id)
    if not user or user.role != Role.REGIONAL_MANAGER:
        raise HTTPException(status_code=404, detail="RM not found")
    before = user.__class__(**{k: getattr(user, k) for k in user.__mapper__.attrs.keys()})
    users_crud.set_active(db, user, False)
    audits_crud.log(db, actor_user_id=str(admin.id), action="DEACTIVATE", entity_type="RegionalManager", entity_id=str(user.id), diff_json=build_diff(before, user), ip=request.client.host if request.client else None)
    return {"message": "RM deactivated"}
