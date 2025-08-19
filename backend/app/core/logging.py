"""
app/core/logging.py

Simple logging setup. In production you can swap to JSON logs or structured logging.
"""
import logging
from app.core.config import settings


def configure_logging() -> None:
    level = logging.DEBUG if settings.DEBUG else logging.INFO
    fmt = "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s"
    logging.basicConfig(level=level, format=fmt)
