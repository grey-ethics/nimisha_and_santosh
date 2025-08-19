"""
app/crud/user.py

Users CRUD helpers (active-only by default where noted).
"""
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, update

from app.models.user import User
from app.core.rbac import Role


class UserCRUD:
    def get_by_id(self, db: Session, user_id: str) -> Optional[User]:
        return db.get(User, user_id)

    def get_by_phone(self, db: Session, phone: str) -> Optional[User]:
        return db.execute(select(User).where(User.phone == phone)).scalar_one_or_none()

    def create(self, db: Session, *, phone: str, password_hash: str, role: Role, full_name: str | None = None, email: str | None = None, must_change_password: bool = False) -> User:
        user = User(phone=phone, password_hash=password_hash, role=role, full_name=full_name, email=email, must_change_password=must_change_password)
        db.add(user)
        db.flush()
        return user

    def list_by_role(self, db: Session, role: Role):
        return db.execute(select(User).where(User.role == role)).scalars().all()

    def set_active(self, db: Session, user: User, is_active: bool) -> User:
        user.is_active = is_active
        db.add(user)
        db.flush()
        return user

    def increment_rtv(self, db: Session, user: User) -> None:
        user.refresh_token_version += 1
        db.add(user)
        db.flush()

    def set_password(self, db: Session, user: User, new_hash: str) -> None:
        user.password_hash = new_hash
        user.must_change_password = False
        db.add(user)
        db.flush()


users = UserCRUD()
