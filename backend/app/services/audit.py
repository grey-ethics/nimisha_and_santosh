"""
app/services/audit.py

Audit diff builder: before/after dicts (JSON-safe).
Converts UUID/Enum/datetime to JSON-serializable primitives and skips relationships.
"""
from typing import Any, Dict
from datetime import date, datetime
from uuid import UUID
from enum import Enum


def _to_jsonable(value: Any) -> Any:
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, (list, tuple)):
        return [_to_jsonable(v) for v in value]
    if isinstance(value, dict):
        return {str(_to_jsonable(k)): _to_jsonable(v) for k, v in value.items()}
    return value


def model_to_safe_dict(obj) -> Dict[str, Any]:
    if obj is None:
        return {}
    data: Dict[str, Any] = {}
    # Only include real table columns; skip relationships/collections
    for col in obj.__mapper__.columns:
        name = col.key
        if name in {"password_hash"}:
            continue
        try:
            data[name] = _to_jsonable(getattr(obj, name))
        except Exception:
            # Be defensive: if anything fails, just skip that field
            pass
    return data


def build_diff(before, after) -> Dict[str, Any]:
    return {
        "before": model_to_safe_dict(before),
        "after": model_to_safe_dict(after),
    }
