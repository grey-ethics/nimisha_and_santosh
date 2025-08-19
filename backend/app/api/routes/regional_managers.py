"""
app/api/routes/regional_managers.py

RM endpoints (scoped to own region):
- BM lifecycle: create/list/patch/deactivate
- GET /patients (read-only, region scope)
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.auth import role_required
from app.core.rbac import Role
from app.db.session import get_db
from app.crud.branch import branches as branches_crud
from app.crud.user import users as users_crud
from app.crud.patient import patients as patients_crud
from app.models.branch_manager_profile import BranchManagerProfile
from app.schemas.user import UserOut
from app.schemas.patient import PatientOut
from app.core.security import hash_password
from app.services.phone import normalize_phone
from app.services.audit import build_diff
from app.crud.audit import audits as audits_crud

router = APIRouter(prefix="/users", tags=["regional-managers"], dependencies=[Depends(role_required(Role.REGIONAL_MANAGER))])


class BranchManagerCreateSchema:
    pass

from pydantic import BaseModel

class BranchManagerCreate(BaseModel):
    phone: str
    password: str
    full_name: str | None = None
    email: str | None = None
    branch_id: str
    notes: str | None = None


class BranchManagerPatch(BaseModel):
    full_name: str | None = None
    email: str | None = None
    branch_id: str | None = None
    notes: str | None = None


@router.post("/branch-managers", response_model=UserOut)
def create_bm(body: BranchManagerCreate, request: Request, db: Session = Depends(get_db), rm=Depends(role_required(Role.REGIONAL_MANAGER))):
    branch = branches_crud.get(db, body.branch_id)
    if not branch or not branch.is_active:
        raise HTTPException(status_code=400, detail="Invalid branch")
    # scope: branch must be in RM's region
    if not rm.regional_manager_profile or str(branch.region_id) != str(rm.regional_manager_profile.region_id):
        raise HTTPException(status_code=403, detail="Branch outside RM region")

    phone = normalize_phone(body.phone)
    if users_crud.get_by_phone(db, phone):
        raise HTTPException(status_code=400, detail="Phone already exists")

    user = users_crud.create(db, phone=phone, password_hash=hash_password(body.password), role=Role.BRANCH_MANAGER, full_name=body.full_name, email=body.email)
    prof = BranchManagerProfile(user_id=user.id, branch_id=branch.id, notes=body.notes)
    db.add(prof)
    db.flush()
    audits_crud.log(db, actor_user_id=str(rm.id), action="CREATE", entity_type="BranchManager", entity_id=str(user.id), diff_json=build_diff(None, user), ip=request.client.host if request.client else None)
    return user


@router.get("/branch-managers", response_model=list[UserOut])
def list_bms(db: Session = Depends(get_db), rm=Depends(role_required(Role.REGIONAL_MANAGER))):
    # list BMs within RM's region
    bms = [u for u in users_crud.list_by_role(db, Role.BRANCH_MANAGER) if u.branch_manager_profile and str(u.branch_manager_profile.branch.region_id) == str(rm.regional_manager_profile.region_id)]
    return bms


@router.patch("/branch-managers/{user_id}", response_model=UserOut)
def patch_bm(user_id: str, body: BranchManagerPatch, request: Request, db: Session = Depends(get_db), rm=Depends(role_required(Role.REGIONAL_MANAGER))):
    user = users_crud.get_by_id(db, user_id)
    if not user or user.role != Role.BRANCH_MANAGER:
        raise HTTPException(status_code=404, detail="BM not found")
    # Scope: BM must be in RM's region
    if not user.branch_manager_profile or str(user.branch_manager_profile.branch.region_id) != str(rm.regional_manager_profile.region_id):
        raise HTTPException(status_code=403, detail="BM outside RM region")

    before = user.__class__(**{k: getattr(user, k) for k in user.__mapper__.attrs.keys()})
    if body.full_name is not None:
        user.full_name = body.full_name
    if body.email is not None:
        user.email = body.email
    if body.branch_id is not None:
        branch = branches_crud.get(db, body.branch_id)
        if not branch or str(branch.region_id) != str(rm.regional_manager_profile.region_id):
            raise HTTPException(status_code=403, detail="New branch outside RM region")
        user.branch_manager_profile.branch_id = branch.id
    if body.notes is not None:
        user.branch_manager_profile.notes = body.notes

    db.add(user)
    db.flush()
    audits_crud.log(db, actor_user_id=str(rm.id), action="UPDATE", entity_type="BranchManager", entity_id=str(user.id), diff_json=build_diff(before, user), ip=None)
    return user


@router.post("/branch-managers/{user_id}:deactivate")
def deactivate_bm(user_id: str, request: Request, db: Session = Depends(get_db), rm=Depends(role_required(Role.REGIONAL_MANAGER))):
    user = users_crud.get_by_id(db, user_id)
    if not user or user.role != Role.BRANCH_MANAGER:
        raise HTTPException(status_code=404, detail="BM not found")
    if not user.branch_manager_profile or str(user.branch_manager_profile.branch.region_id) != str(rm.regional_manager_profile.region_id):
        raise HTTPException(status_code=403, detail="BM outside RM region")
    before = user.__class__(**{k: getattr(user, k) for k in user.__mapper__.attrs.keys()})
    users_crud.set_active(db, user, False)
    audits_crud.log(db, actor_user_id=str(rm.id), action="DEACTIVATE", entity_type="BranchManager", entity_id=str(user.id), diff_json=build_diff(before, user), ip=request.client.host if request.client else None)
    return {"message": "BM deactivated"}


@router.get("/patients", response_model=list[PatientOut])
def list_patients_region(db: Session = Depends(get_db), rm=Depends(role_required(Role.REGIONAL_MANAGER))):
    # collect branch ids for region
    region_id = str(rm.regional_manager_profile.region_id)
    branch_ids = [str(b.id) for b in rm.regional_manager_profile.region.branches if b.is_active]
    return patients_crud.list_by_region(db, branch_ids)
