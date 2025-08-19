"""
app/schemas/branch.py
"""
from pydantic import BaseModel, ConfigDict


class BranchCreate(BaseModel):
    region_id: str
    name: str
    address: str | None = None


class BranchOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    region_id: str
    name: str
    address: str | None
    is_active: bool
