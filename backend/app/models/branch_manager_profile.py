"""
app/models/branch_manager_profile.py

Branch Manager Profile: links user -> branch.
"""
import uuid
from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class BranchManagerProfile(Base):
    __tablename__ = "branch_manager_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    branch_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("branches.id", ondelete="RESTRICT"), nullable=False)
    notes: Mapped[str | None] = mapped_column(String(2000))

    user = relationship("User", back_populates="branch_manager_profile")
    branch = relationship("Branch", back_populates="branch_managers")
