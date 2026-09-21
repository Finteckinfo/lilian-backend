from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import store
from app.config import settings
from app.db import has_supabase
from app.routers import admin, auth, leads, portfolio, posts
from app import users as user_store


@asynccontextmanager
async def lifespan(_app: FastAPI):
    store.load_persisted()
    # Fail fast in production if auth secret missing
    if settings.is_production:
        settings.jwt_secret()
    yield


app = FastAPI(
    title="Being Lillian API",
    version="1.1.0",
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
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or default_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(portfolio.router)
app.include_router(leads.router)
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
