import re
import time
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app import users as user_store
from app.config import settings

_hits: dict[str, list[float]] = defaultdict(list)
_bearer = HTTPBearer(auto_error=False)


def client_ip(request: Request) -> str:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    if request.client:
        return request.client.host
    return "local"


def _rate_limit(bucket: str, limit: int, window: int) -> None:
    now = time.time()
    recent = [t for t in _hits[bucket] if now - t < window]
    if len(recent) >= limit:
        raise HTTPException(status_code=429, detail="Too many requests")
    recent.append(now)
    _hits[bucket] = recent


def rate_limit_leads(request: Request) -> None:
    _rate_limit(
        f"leads:{client_ip(request)}",
        settings.lead_rate_limit,
        settings.lead_rate_window_seconds,
    )


def rate_limit_auth(request: Request) -> None:
    _rate_limit(
        f"auth:{client_ip(request)}",
        settings.auth_rate_limit,
        settings.auth_rate_window_seconds,
    )


def normalize_phone(phone: str) -> str:
    cleaned = re.sub(r"[^\d+]", "", phone.strip())
    digits = re.sub(r"\D", "", cleaned)
    if len(digits) < 7:
        raise HTTPException(status_code=400, detail="Invalid phone number")
    return cleaned


def create_access_token(user: dict[str, Any]) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user["id"]),
        "email": user["email"],
        "role": user.get("role") or "admin",
        "iss": "being-lillian",
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=settings.auth_jwt_hours)).timestamp()),
    }
    return jwt.encode(payload, settings.jwt_secret(), algorithm="HS256")


def _decode_studio_jwt(token: str) -> dict[str, Any] | None:
    try:
        return jwt.decode(
            token,
            settings.jwt_secret(),
            algorithms=["HS256"],
            options={"require_exp": True},
        )
    except JWTError:
        return None


def _decode_supabase_jwt(token: str) -> dict[str, Any] | None:
    if not settings.supabase_jwt_secret:
        return None
    try:
        return jwt.decode(
            token,
            settings.supabase_jwt_secret,
            algorithms=["HS256"],
            audience="authenticated",
        )
    except JWTError:
        return None


def verify_admin_jwt(request: Request) -> dict[str, Any]:
    auth = request.headers.get("authorization") or ""
    if not auth.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing bearer token",
        )
    token = auth.split(" ", 1)[1].strip()
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")

    payload = _decode_studio_jwt(token)
    if payload and payload.get("iss") == "being-lillian":
        user = user_store.find_by_id(str(payload.get("sub") or ""))
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return {
            "sub": user["id"],
            "email": user["email"],
            "role": user.get("role") or "admin",
            "full_name": user.get("full_name"),
            "auth": "studio",
        }

    payload = _decode_supabase_jwt(token)
    if payload:
        return {
            "sub": str(payload.get("sub") or ""),
            "email": payload.get("email"),
            "role": payload.get("role") or "authenticated",
            "auth": "supabase",
        }

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")


AdminUser = dict


def require_admin(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
) -> AdminUser:
    _ = credentials  # ensures OpenAPI shows bearer
    return verify_admin_jwt(request)
