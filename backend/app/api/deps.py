"""
app/api/deps.py

Shared API dependencies (pagination etc.).
"""
from fastapi import Query
from app.utils.pagination import PageParams


def pagination(limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0)) -> PageParams:
    return PageParams(limit=limit, offset=offset)
