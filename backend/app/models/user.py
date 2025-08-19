"""
app/models/user.py

User model (single table, roles via enum).
Includes refresh_token_version for refresh rotation (simple, per-user).
"""
import uuid
from datetime import datetime
from sqlalchemy import Boolean, Enum, String, text, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.rbac import Role
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    # --- Columns ---
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role: Mapped[Role] = mapped_column(Enum(Role, name="role_enum", create_constraint=True), nullable=False)

    phone: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(200), nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(200))
    email: Mapped[str | None] = mapped_column(String(200))

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("true"))
    must_change_password: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default=text("false"))
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # refresh token version for rotation
    refresh_token_version: Mapped[int] = mapped_column(Integer, nullable=False, server_default=text("0"))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=datetime.utcnow,
    )

    # --- Relationships ---
    regional_manager_profile = relationship("RegionalManagerProfile", back_populates="user", uselist=False)
    branch_manager_profile   = relationship("BranchManagerProfile",   back_populates="user", uselist=False)

    # Disambiguate which FK in patient_profiles points to this relationship.
    # patient_profiles has user_id, assigned_bm_user_id, created_by_user_id -> users.id
    patient_profile = relationship(
        "PatientProfile",
        back_populates="user",
        uselist=False,
        foreign_keys="PatientProfile.user_id",  # <-- the crucial fix
    )
