"""
app/schemas/audit.py
"""
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AuditOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    actor_user_id: UUID | None
    action: str
    entity_type: str
    entity_id: UUID | None
    diff_json: dict | None
    timestamp: datetime
    ip: str | None
