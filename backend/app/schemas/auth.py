"""
app/schemas/auth.py

Auth schemas (Pydantic v2).
"""
from pydantic import BaseModel, ConfigDict, Field


class LoginRequest(BaseModel):
    phone: str
    password: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    must_change_password: bool = False


class RefreshRequest(BaseModel):
    refresh_token: str


class ChangePasswordRequest(BaseModel):
    current_password: str | None = None  # required unless must_change_password
    new_password: str = Field(min_length=8)
