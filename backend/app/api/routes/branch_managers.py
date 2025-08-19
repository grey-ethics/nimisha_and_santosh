"""
app/api/routes/branch_managers.py

BM endpoints (branch-scoped):
- Patients: create/list/get/patch/deactivate/(assign)
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.core.auth import role_required
from app.core.rbac import Role
from app.db.session import get_db
from app.schemas.patient import PatientCreate, PatientOut, PatientUpdate
from app.crud.patient import patients as patients_crud
from app.crud.user import users as users_crud
from app.core.security import hash_password
from app.services.phone import normalize_phone
from app.services.audit import build_diff
from app.crud.audit import audits as audits_crud
from app.models.user import User

router = APIRouter(prefix="/patients", tags=["branch-managers"], dependencies=[Depends(role_required(Role.BRANCH_MANAGER))])


@router.post("", response_model=PatientOut)
def create_patient(body: PatientCreate, request: Request, db: Session = Depends(get_db), bm=Depends(role_required(Role.BRANCH_MANAGER))):
    if str(body.branch_id) != str(bm.branch_manager_profile.branch_id):
        raise HTTPException(status_code=403, detail="Branch mismatch")

    # create patient user
    phone = normalize_phone(body.phone)
    if users_crud.get_by_phone(db, phone):
        raise HTTPException(status_code=400, detail="Phone already exists")

    patient_user = users_crud.create(db, phone=phone, password_hash=hash_password(body.password), role=Role.PATIENT, full_name=body.full_name, email=body.email, must_change_password=True)

    patient = patients_crud.create(
        db,
        user=patient_user,
        branch_id=body.branch_id,
        assigned_bm_user_id=body.assigned_bm_user_id,
        created_by_user_id=str(bm.id),
        rm_approval=body.rm_approval,
        enrollment_date=body.enrollment_date,
        transplant_date=body.transplant_date,
        notes=body.notes,
        mrn=body.mrn,
        blood_group=body.blood_group,
        donor_type=body.donor_type,
        primary_center=body.primary_center,
        treating_physician=body.treating_physician,
        date_of_birth=body.date_of_birth,
        gender=body.gender,
        emergency_contact_name=body.emergency_contact_name,
        emergency_contact_phone=body.emergency_contact_phone,
        status=body.status,
    )
    audits_crud.log(db, actor_user_id=str(bm.id), action="CREATE", entity_type="Patient", entity_id=str(patient.user_id), diff_json=build_diff(None, patient), ip=request.client.host if request.client else None)
    return patient


@router.get("", response_model=list[PatientOut])
def list_patients(db: Session = Depends(get_db), bm=Depends(role_required(Role.BRANCH_MANAGER))):
    return patients_crud.list_by_branch(db, str(bm.branch_manager_profile.branch_id))


@router.get("/{user_id}", response_model=PatientOut)
def get_patient(user_id: str, db: Session = Depends(get_db), bm=Depends(role_required(Role.BRANCH_MANAGER))):
    patient = patients_crud.get(db, user_id)
    if not patient or not patient.is_active or str(patient.branch_id) != str(bm.branch_manager_profile.branch_id):
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.patch("/{user_id}", response_model=PatientOut)
def update_patient(user_id: str, body: PatientUpdate, request: Request, db: Session = Depends(get_db), bm=Depends(role_required(Role.BRANCH_MANAGER))):
    patient = patients_crud.get(db, user_id)
    if not patient or str(patient.branch_id) != str(bm.branch_manager_profile.branch_id):
        raise HTTPException(status_code=404, detail="Patient not found")
    before = patient.__class__(**{k: getattr(patient, k) for k in patient.__mapper__.attrs.keys()})

    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(patient, field, value)

    db.add(patient)
    db.flush()
    audits_crud.log(db, actor_user_id=str(bm.id), action="UPDATE", entity_type="Patient", entity_id=str(patient.user_id), diff_json=build_diff(before, patient), ip=request.client.host if request.client else None)
    return patient


@router.post("/{user_id}:deactivate")
def deactivate_patient(user_id: str, request: Request, db: Session = Depends(get_db), bm=Depends(role_required(Role.BRANCH_MANAGER))):
    patient = patients_crud.get(db, user_id)
    if not patient or str(patient.branch_id) != str(bm.branch_manager_profile.branch_id):
        raise HTTPException(status_code=404, detail="Patient not found")
    before = patient.__class__(**{k: getattr(patient, k) for k in patient.__mapper__.attrs.keys()})
    patients_crud.deactivate(db, patient)
    audits_crud.log(db, actor_user_id=str(bm.id), action="DEACTIVATE", entity_type="Patient", entity_id=str(patient.user_id), diff_json=build_diff(before, patient), ip=request.client.host if request.client else None)
    return {"message": "Patient deactivated"}
