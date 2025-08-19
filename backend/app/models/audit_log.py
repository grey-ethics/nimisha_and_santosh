"""
app/models/audit_log.py

Audit logs for CREATE/UPDATE/DEACTIVATE actions on administrative writes.
"""

import uuid
from datetime import datetime
from enum import Enum as PyEnum  # ✅ use Python Enum here

from sqlalchemy import String, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID, INET
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


# --- Correct Enum class ---
class AuditAction(str, PyEnum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DEACTIVATE = "DEACTIVATE"


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    actor_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    # ✅ Use SQLAlchemy Enum type with our Python Enum
    action: Mapped[AuditAction] = mapped_column(Enum(AuditAction, name="audit_action"), nullable=False)

    entity_type: Mapped[str] = mapped_column(String(64), nullable=False)
    entity_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    diff_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    ip: Mapped[str | None] = mapped_column(INET, nullable=True)

    actor = relationship("User")
