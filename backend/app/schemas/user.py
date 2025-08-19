"""
app/schemas/user.py

User schemas for responses. Avoid secrets.
"""
from pydantic import BaseModel, ConfigDict
from app.core.rbac import Role


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    role: Role
    phone: str
    full_name: str | None
    email: str | None
    is_active: bool
    must_change_password: bool
