"""
app/utils/pagination.py

Simple limit/offset parameters & result wrapper.
"""
from pydantic import BaseModel, Field


class PageParams(BaseModel):
    limit: int = Field(default=50, ge=1, le=200)
    offset: int = Field(default=0, ge=0)
