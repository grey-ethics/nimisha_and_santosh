# FILE: scripts/seed_admin.py
"""
Quickly create a Super Admin (role=ADMIN) in the shared 'users' table.

This version is hard-coded with fixed credentials.
Just run:
    python scripts/seed_admin.py

Notes:
- Admins are rows in `users` with role='ADMIN'.
- If the admin already exists, the script will not duplicate it.
"""

from __future__ import annotations

import sys
from pathlib import Path

# --- Ensure we can import the 'app' package when running as a script ---
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# --- Load .env before importing settings/engine ---
from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

from app.core.rbac import Role
from app.core.security import hash_password
from app.services.phone import normalize_phone
from app.db.base import Base
from app.db.session import engine, SessionLocal
from app.crud.user import users
import app.models  # noqa: F401  # ensure models are registered with Base


def ensure_tables() -> None:
    """Create tables if Alembic hasn't run yet (idempotent)."""
    Base.metadata.create_all(bind=engine)


def main() -> None:
    ensure_tables()

    # --- Hard-coded Super Admin values ---
    phone_raw = "+919876543210"
    password_raw = "SuperPassword@123"
    full_name = "Super Admin"

    # Normalize phone format
    phone = normalize_phone(phone_raw)

    with SessionLocal() as db:
        # Check if user already exists
        existing = users.get_by_phone(db, phone)
        if existing:
            if existing.role == Role.ADMIN:
                print(f"ℹ️ Admin already exists: {existing.id} ({existing.phone})")
            else:
                print(f"ℹ️ A user with {phone} exists with role={existing.role}; not modifying.")
            return

        # Create Admin
        admin = users.create(
            db,
            phone=phone,
            password_hash=hash_password(password_raw),
            role=Role.ADMIN,
            full_name=full_name,
            email=None,
        )
        db.commit()

        print("✅ Super Admin created successfully!")
        print(f"   ID:    {admin.id}")
        print(f"   Phone: {admin.phone}")
        print(f"   Name:  {admin.full_name or ''}".rstrip())
        print(f"\nYou can now log in with phone={phone_raw} and password={password_raw}")


if __name__ == "__main__":
    main()
