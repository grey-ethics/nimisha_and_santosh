"""
app/schemas/patient.py
"""
from uuid import UUID
from datetime import date
from pydantic import BaseModel, ConfigDict, Field, field_validator
from app.core.rbac import DonorType, PatientStatus, Gender


class PatientBase(BaseModel):
    # Request fields can remain strings; switching to UUID is optional.
    branch_id: str
    assigned_bm_user_id: str
    rm_approval: bool = False
    enrollment_date: date | None = None
    transplant_date: date | None = None
    notes: str | None = None

    mrn: str | None = None
    blood_group: str | None = None
    donor_type: DonorType | None = None
    primary_center: str | None = None
    treating_physician: str | None = None
    date_of_birth: date | None = None
    gender: Gender | None = None
    emergency_contact_name: str | None = None
    emergency_contact_phone: str | None = None

    status: PatientStatus = PatientStatus.ACTIVE

    @field_validator("transplant_date")
    @classmethod
    def validate_transplant_date(cls, v: date | None):
        from datetime import date as _date
        if v and v > _date.today():
            raise ValueError("transplant_date cannot be in the future")
        return v

    @field_validator("date_of_birth")
    @classmethod
    def validate_dob(cls, v: date | None):
        from datetime import date as _date
        if v and v >= _date.today():
            raise ValueError("date_of_birth must be in the past")
        return v


class PatientCreate(PatientBase):
    phone: str
    password: str
    full_name: str | None = None
    email: str | None = None


class PatientUpdate(BaseModel):
    # editable subset
    rm_approval: bool | None = None
    enrollment_date: date | None = None
    transplant_date: date | None = None
    notes: str | None = None
    mrn: str | None = None
    blood_group: str | None = None
    donor_type: DonorType | None = None
    primary_center: str | None = None
    treating_physician: str | None = None
    date_of_birth: date | None = None
    gender: Gender | None = None
    emergency_contact_name: str | None = None
    emergency_contact_phone: str | None = None
    status: PatientStatus | None = None


class PatientOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: UUID
    branch_id: UUID
    assigned_bm_user_id: UUID
    rm_approval: bool
    enrollment_date: date | None
    transplant_date: date | None
    notes: str | None
    mrn: str | None
    blood_group: str | None
    donor_type: DonorType | None
    primary_center: str | None
    treating_physician: str | None
    date_of_birth: date | None
    gender: Gender | None
    emergency_contact_name: str | None
    emergency_contact_phone: str | None
    status: PatientStatus
    is_active: bool
