"""
app/crud/region.py

Region CRUD and listing (active by default).
"""
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.region import Region


class RegionCRUD:
    def create(self, db: Session, name: str) -> Region:
        r = Region(name=name)
        db.add(r)
        db.flush()
        return r

    def get(self, db: Session, region_id: str) -> Optional[Region]:
        return db.get(Region, region_id)

    def list(self, db: Session):
        return db.execute(select(Region).where(Region.is_active.is_(True))).scalars().all()


regions = RegionCRUD()
