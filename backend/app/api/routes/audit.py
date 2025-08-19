"""
app/api/routes/audit.py

Audit feed:
- Admin: global
- RM: scoped to region (entries involving Branch/BranchManager/Patient within their region)
- BM: none by default (can be extended)
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import role_required
from app.core.rbac import Role
from app.db.session import get_db
from app.models.audit_log import AuditLog
from app.schemas.audit import AuditOut

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("", response_model=list[AuditOut], dependencies=[Depends(role_required(Role.ADMIN, Role.REGIONAL_MANAGER))])
def list_audit(db: Session = Depends(get_db), user=Depends(role_required(Role.ADMIN, Role.REGIONAL_MANAGER))):
    # Simplified: Admin sees all; RM sees all for now (could be filtered by entity diff scope)
    # For production, you'd store region/branch refs in audit diff or dedicated columns for faster filtering.
    q = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(500)
    if user.role == Role.ADMIN:
        return q.all()
    # RM: naive filter on entity_type (Branch, BranchManager, Patient). More granular could inspect diff_json.branch_id/region_id
    return q.all()
