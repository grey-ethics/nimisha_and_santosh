"""
app/schemas/region.py
"""
from pydantic import BaseModel, ConfigDict


class RegionCreate(BaseModel):
    name: str


class RegionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str
    is_active: bool
