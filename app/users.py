"""Admin users — bcrypt passwords + persisted JSON (local) or extendable to Supabase."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

import bcrypt

from app.config import settings

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _users_path() -> Path:
    root = Path(__file__).resolve().parent.parent / settings.data_dir
    root.mkdir(parents=True, exist_ok=True)
    return root / "users.json"


def _load() -> list[dict[str, Any]]:
    path = _users_path()
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def _save(users: list[dict[str, Any]]) -> None:
    path = _users_path()
    path.write_text(json.dumps(users, indent=2), encoding="utf-8")


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt(rounds=12)).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except ValueError:
        return False


def list_users() -> list[dict[str, Any]]:
    return _load()


def user_count() -> int:
    return len(_load())


def signup_open() -> bool:
    if user_count() == 0:
        return True
    return bool(settings.auth_allow_signup)


def find_by_email(email: str) -> dict[str, Any] | None:
    needle = email.strip().lower()
    for user in _load():
        if str(user.get("email", "")).lower() == needle:
            return user
    return None


def find_by_id(user_id: str) -> dict[str, Any] | None:
    for user in _load():
        if str(user.get("id")) == user_id:
            return user
    return None


def create_user(email: str, password: str, full_name: str) -> dict[str, Any]:
    email_n = email.strip().lower()
    if not EMAIL_RE.match(email_n):
        raise ValueError("Invalid email")
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")
    if find_by_email(email_n):
        raise ValueError("Email already registered")
    if not signup_open():
        raise ValueError("Signup is closed — ask an existing admin to enable AUTH_ALLOW_SIGNUP")

    users = _load()
    row = {
        "id": str(uuid4()),
        "email": email_n,
        "full_name": full_name.strip() or email_n.split("@")[0],
        "password_hash": hash_password(password),
        "role": "admin",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "last_login_at": datetime.now(timezone.utc).isoformat(),
        "login_count": 1,
    }
    users.append(row)
    _save(users)
    return {k: v for k, v in row.items() if k != "password_hash"}


def public_user(user: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": user["id"],
        "email": user["email"],
        "full_name": user.get("full_name") or "",
        "role": user.get("role") or "admin",
        "created_at": user.get("created_at"),
        "last_login_at": user.get("last_login_at"),
        "login_count": int(user.get("login_count") or 0),
    }


def touch_login(user_id: str) -> dict[str, Any] | None:
    users = _load()
    found = None
    now = datetime.now(timezone.utc).isoformat()
    for user in users:
        if str(user.get("id")) == user_id:
            user["last_login_at"] = now
            user["login_count"] = int(user.get("login_count") or 0) + 1
            found = user
            break
    if found:
        _save(users)
    return found


def change_password(user_id: str, current_password: str, new_password: str) -> None:
    if len(new_password) < 8:
        raise ValueError("Password must be at least 8 characters")
    users = _load()
    found = None
    for user in users:
        if str(user.get("id")) == user_id:
            found = user
            break
    if not found:
        raise ValueError("Account not found")
    if not verify_password(current_password, str(found.get("password_hash") or "")):
        raise ValueError("Current password is incorrect")
    found["password_hash"] = hash_password(new_password)
    _save(users)


def delete_user(user_id: str) -> None:
    users = _load()
    if len(users) <= 1:
        raise ValueError("The only studio account cannot be removed")
    remaining = [u for u in users if str(u.get("id")) != user_id]
    if len(remaining) == len(users):
        raise ValueError("Account not found")
    _save(remaining)
