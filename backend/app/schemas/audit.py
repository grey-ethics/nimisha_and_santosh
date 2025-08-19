"""
app/schemas/audit.py
"""
from pydantic import BaseModel, ConfigDict


class AuditOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    actor_user_id: str | None
    action: str
    entity_type: str
    entity_id: str | None
    diff_json: dict | None
    timestamp: str
    ip: str | None
