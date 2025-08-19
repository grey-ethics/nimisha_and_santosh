"""
app/db/base.py

SQLAlchemy declarative Base.
Keep this file free of model imports to avoid circular imports.
Alembic will import models in migrations/env.py to populate metadata.
"""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all models."""
    pass
