from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app import store
from app.config import settings
from app.db import has_supabase
from app.routers import admin, auth, catalog, leads, portfolio, posts
from app import users as user_store


@asynccontextmanager
async def lifespan(_app: FastAPI):
    store.load_persisted()
    if settings.is_production:
        settings.jwt_secret()
    yield


app = FastAPI(
    title="Being Lillian API",
    version="1.2.0",
    lifespan=lifespan,
    docs_url=None if settings.is_production else "/docs",
    redoc_url=None if settings.is_production else "/redoc",
    openapi_url=None if settings.is_production else "/openapi.json",
)

origins = [o.strip() for o in settings.frontend_origin.split(",") if o.strip()]
default_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
production_origins = [
    "https://beinglillian.com",
    "https://www.beinglillian.com",
]
allow_origins = list(dict.fromkeys([*(origins or default_origins), *production_origins]))
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        if settings.is_production:
            response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains"
        return response


app.add_middleware(SecurityHeadersMiddleware)

app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(portfolio.router)
app.include_router(leads.router)
app.include_router(catalog.router)
app.include_router(admin.router)


@app.get("/health")
def health():
    return {"ok": True, "supabase": has_supabase(), "env": settings.environment}


@app.get("/health/ready")
def ready():
    return {
        "ok": True,
        "supabase": has_supabase(),
        "users": user_store.user_count(),
        "signup_open": user_store.signup_open(),
        "posts": len(store.LOCAL_POSTS),
        "portfolio": len(store.LOCAL_PORTFOLIO),
        "leads": len(store.LOCAL_LEADS),
    }
