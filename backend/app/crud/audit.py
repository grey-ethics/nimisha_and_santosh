"""
app/crud/audit.py

AuditLog persisters.
"""
from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog


class AuditCRUD:
    def log(self, db: Session, *, actor_user_id: str | None, action: str, entity_type: str, entity_id: str | None, diff_json: dict | None, ip: str | None) -> AuditLog:
        entry = AuditLog(actor_user_id=actor_user_id, action=action, entity_type=entity_type, entity_id=entity_id, diff_json=diff_json, ip=ip)
        db.add(entry)
        db.flush()
        return entry


audits = AuditCRUD()
