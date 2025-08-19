"""
app/utils/crypto.py

Small crypto helpers (e.g., secure randoms if needed later).
"""
import secrets


def secure_token(nbytes: int = 32) -> str:
    return secrets.token_urlsafe(nbytes)
