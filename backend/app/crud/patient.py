"""
app/crud/patient.py

Patient CRUD with soft-deletes and scope-aware helpers.
"""
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.rbac import PatientStatus
from app.models.patient_profile import PatientProfile
from app.models.user import User


class PatientCRUD:
    def create(self, db: Session, *, user: User, branch_id: str, assigned_bm_user_id: str, created_by_user_id: str, **kwargs) -> PatientProfile:
        p = PatientProfile(
            user_id=user.id,
            branch_id=branch_id,
            assigned_bm_user_id=assigned_bm_user_id,
            created_by_user_id=created_by_user_id,
            **kwargs,
        )
        db.add(p)
        db.flush()
        return p

    def get(self, db: Session, user_id: str) -> Optional[PatientProfile]:
        return db.get(PatientProfile, user_id)

    def list_by_branch(self, db: Session, branch_id: str) -> List[PatientProfile]:
        stmt = select(PatientProfile).where(PatientProfile.branch_id == branch_id, PatientProfile.is_active.is_(True))
        return db.execute(stmt).scalars().all()

    def list_by_region(self, db: Session, region_branch_ids: list[str]) -> List[PatientProfile]:
        if not region_branch_ids:
            return []
        stmt = select(PatientProfile).where(PatientProfile.branch_id.in_(region_branch_ids), PatientProfile.is_active.is_(True))
        return db.execute(stmt).scalars().all()

    def deactivate(self, db: Session, patient: PatientProfile) -> PatientProfile:
        patient.is_active = False
        patient.status = PatientStatus.INACTIVE
        db.add(patient)
        db.flush()
        return patient


patients = PatientCRUD()
