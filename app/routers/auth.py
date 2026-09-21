from fastapi import APIRouter, Depends, HTTPException, Request

from app import users as user_store
from app.auth import create_access_token, rate_limit_auth, require_admin
from app.schemas.models import AuthLogin, AuthSignup, AuthTokenOut, AuthUserOut
from app import store

router = APIRouter(tags=["auth"])


@router.get("/v1/auth/status")
def auth_status():
    return {
        "has_users": user_store.user_count() > 0,
        "signup_open": user_store.signup_open(),
    }


@router.post("/v1/auth/signup", response_model=AuthTokenOut, status_code=201)
def signup(payload: AuthSignup, request: Request):
    rate_limit_auth(request)
    try:
        user = user_store.create_user(payload.email, payload.password, payload.full_name)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    full = user_store.find_by_id(user["id"]) or user
    token = create_access_token(full)
    store.log_activity("auth", f"Admin signup: {user['email']}", {"id": user["id"]})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user_store.public_user(full) if "password_hash" in full else user,
    }


@router.post("/v1/auth/login", response_model=AuthTokenOut)
def login(payload: AuthLogin, request: Request):
    rate_limit_auth(request)
    user = user_store.find_by_email(payload.email)
    if not user or not user_store.verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token(user)
    store.log_activity("auth", f"Admin login: {user['email']}", {"id": user["id"]})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user_store.public_user(user),
    }


@router.get("/v1/auth/me", response_model=AuthUserOut)
def me(admin=Depends(require_admin)):
    if admin.get("auth") == "studio":
        user = user_store.find_by_id(str(admin.get("sub") or ""))
        if user:
            return user_store.public_user(user)
    return {
        "id": str(admin.get("sub") or ""),
        "email": str(admin.get("email") or ""),
        "full_name": str(admin.get("full_name") or admin.get("email") or ""),
        "role": str(admin.get("role") or "admin"),
        "created_at": None,
    }
