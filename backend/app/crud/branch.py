"""
app/crud/branch.py

Branch CRUD; ensures active-only listings by default.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.branch import Branch


class BranchCRUD:
    def create(self, db: Session, *, region_id: str, name: str, address: str | None) -> Branch:
        b = Branch(region_id=region_id, name=name, address=address)
        db.add(b)
        db.flush()
        return b

    def get(self, db: Session, branch_id: str) -> Optional[Branch]:
        return db.get(Branch, branch_id)

    def list_by_region(self, db: Session, region_id: str) -> List[Branch]:
        return db.execute(select(Branch).where(Branch.region_id == region_id, Branch.is_active.is_(True))).scalars().all()


branches = BranchCRUD()
