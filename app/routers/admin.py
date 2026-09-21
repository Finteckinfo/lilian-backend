from collections import Counter

from fastapi import APIRouter, Depends

from app.auth import require_admin
from app.db import has_supabase
from app.schemas.models import SiteSettings, SiteSettingsPatch
from app import store
from app.seed import LOCAL_LEADS

router = APIRouter(tags=["admin"])


@router.get("/v1/settings", response_model=SiteSettings)
def public_settings():
    return store.get_settings()


@router.get("/v1/admin/settings", response_model=SiteSettings)
def admin_get_settings(_admin=Depends(require_admin)):
    return store.get_settings()


@router.patch("/v1/admin/settings", response_model=SiteSettings)
def admin_patch_settings(payload: SiteSettingsPatch, _admin=Depends(require_admin)):
    patch = payload.model_dump(exclude_unset=True)
    return store.update_settings(patch)


@router.get("/v1/admin/stats")
def admin_stats(_admin=Depends(require_admin)):
    leads = list(LOCAL_LEADS)
    by_status = Counter(str(l.get("status") or "New") for l in leads)
    by_service = Counter(str(l.get("service_type") or "General") for l in leads)
    posts = store.get_posts()
    portfolio = store.get_portfolio()
    return {
        "mode": "supabase" if has_supabase() else "local",
        "leads_total": len(leads),
        "leads_by_status": dict(by_status),
        "leads_by_service": dict(by_service),
        "posts_total": len(posts),
        "posts_featured": sum(1 for p in posts if p.get("is_featured")),
        "portfolio_total": len(portfolio),
        "portfolio_videos": sum(1 for i in portfolio if i.get("media_type") == "Video"),
        "recent_leads": sorted(leads, key=lambda x: x.get("created_at", ""), reverse=True)[:8],
        "activity": store.activity_feed(30),
        "settings": store.get_settings(),
    }
