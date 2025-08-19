"""
app/core/rbac.py

RBAC enums and helpers for role/scope checks.
- Role enum matches DB.
- Scope rules: Admin (global), RM (region), BM (branch), Patient (branch).
"""
from enum import Enum


class Role(str, Enum):
    ADMIN = "ADMIN"
    REGIONAL_MANAGER = "REGIONAL_MANAGER"
    BRANCH_MANAGER = "BRANCH_MANAGER"
    PATIENT = "PATIENT"


class DonorType(str, Enum):
    LIVING = "LIVING"
    DECEASED = "DECEASED"
    UNKNOWN = "UNKNOWN"


class PatientStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"
    UNKNOWN = "UNKNOWN"
