"""
app/services/phone.py

Phone normalization to E.164 when possible using `phonenumbers`.
Fallback: keep only digits, optionally prefix '+'.
"""
import re
from app.core.config import settings

try:
    import phonenumbers
except Exception:  # pragma: no cover
    phonenumbers = None


def normalize_phone(raw: str) -> str:
    raw = (raw or "").strip()
    if not raw:
        return raw
    if phonenumbers:
        try:
            num = phonenumbers.parse(raw, settings.E164_DEFAULT_COUNTRY or "IN")
            if phonenumbers.is_valid_number(num):
                return phonenumbers.format_number(num, phonenumbers.PhoneNumberFormat.E164)
        except Exception:
            pass
    # Fallback: keep digits and leading plus
    digits = re.sub(r"[^\d+]", "", raw)
    if not digits.startswith("+"):
        digits = "+" + digits
    return digits
