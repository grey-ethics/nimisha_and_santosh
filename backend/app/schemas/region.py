"""
app/schemas/region.py
"""
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class RegionCreate(BaseModel):
    name: str


class RegionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    is_active: bool
