"""
app/services/audit.py

Audit diff builder: before/after dicts for tracked models.
Use only safe fields (no secrets).
"""
from typing import Any, Dict
from sqlalchemy.orm import InstanceState


def model_to_safe_dict(obj) -> Dict[str, Any]:
    if obj is None:
        return {}
    data = {}
    for k in obj.__mapper__.attrs.keys():
        if k in {"password_hash"}:
            continue
        try:
            data[k] = getattr(obj, k)
        except Exception:
            pass
    return data


def build_diff(before, after) -> Dict[str, Any]:
    return {
        "before": model_to_safe_dict(before),
        "after": model_to_safe_dict(after),
    }
