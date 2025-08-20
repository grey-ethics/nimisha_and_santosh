"""
app/schemas/branch.py
"""
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class BranchCreate(BaseModel):
    # Request body can stay as string if you prefer; UUID also works.
    region_id: str
    name: str
    address: str | None = None


class BranchOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    region_id: UUID
    name: str
    address: str | None
    is_active: bool
