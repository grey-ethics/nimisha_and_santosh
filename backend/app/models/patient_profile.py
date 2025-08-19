"""
app/models/patient_profile.py

Patient Profile, with optional clinical and contact fields.
Enforces assignment to a Branch and a BM user (role=BM).
"""
import uuid
from datetime import date, datetime
from sqlalchemy import Date, DateTime, Enum, ForeignKey, String, text, Boolean, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.rbac import DonorType, PatientStatus, Gender
from app.db.base import Base


class PatientProfile(Base):
    __tablename__ = "patient_profiles"
    __table_args__ = (
        UniqueConstraint("branch_id", "mrn", name="uq_patient_mrn_in_branch"),
    )

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    branch_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("branches.id", ondelete="RESTRICT"), nullable=False)
    assigned_bm_user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)

    rm_approval: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("false"))
    enrollment_date: Mapped[date | None] = mapped_column(Date)
    transplant_date: Mapped[date | None] = mapped_column(Date)
    notes: Mapped[str | None] = mapped_column(String(2000))

    mrn: Mapped[str | None] = mapped_column(String(64))
    blood_group: Mapped[str | None] = mapped_column(String(8))
    donor_type: Mapped[DonorType | None] = mapped_column(Enum(DonorType, name="donor_type_enum", create_constraint=True))
    primary_center: Mapped[str | None] = mapped_column(String(200))
    treating_physician: Mapped[str | None] = mapped_column(String(200))
    date_of_birth: Mapped[date | None] = mapped_column(Date)
    gender: Mapped[Gender | None] = mapped_column(Enum(Gender, name="gender_enum", create_constraint=True))
    emergency_contact_name: Mapped[str | None] = mapped_column(String(200))
    emergency_contact_phone: Mapped[str | None] = mapped_column(String(32))

    status: Mapped[PatientStatus] = mapped_column(Enum(PatientStatus, name="patient_status_enum", create_constraint=True), nullable=False, server_default=text("'ACTIVE'"))
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("true"))

    created_by_user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))

    user = relationship("User", back_populates="patient_profile", foreign_keys=[user_id])
    branch = relationship("Branch", back_populates="patients")
    assigned_bm_user = relationship("User", foreign_keys=[assigned_bm_user_id])
    created_by_user = relationship("User", foreign_keys=[created_by_user_id])
