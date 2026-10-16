from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Response

from app.auth import require_admin
from app.db import get_supabase
from app.schemas.models import PortfolioOut, PortfolioWrite
from app import store

router = APIRouter(tags=["portfolio"])


def _map_item(row: dict) -> dict:
    cat = row["category"]
    media = row["media_type"]
    return {
        "id": str(row.get("id")),
        "title": row["title"],
        "category": cat.value if hasattr(cat, "value") else cat,
        "media_type": media.value if hasattr(media, "value") else media,
        "media_url": row["media_url"],
        "video_url": row.get("video_url"),
        "instagram_url": row.get("instagram_url"),
        "testimonial_text": row.get("testimonial_text"),
        "display_order": int(row.get("display_order") or 0),
    }


def _list_local() -> list[dict]:
    return [_map_item(i) for i in store.get_portfolio()]


@router.get("/v1/portfolio", response_model=list[PortfolioOut])
def list_portfolio():
    db = get_supabase()
    if db:
        res = db.table("portfolio_items").select("*").order("display_order").execute()
        if res.data:
            return [_map_item(r) for r in res.data]
    return _list_local()


@router.get("/v1/admin/portfolio", response_model=list[PortfolioOut])
def admin_list_portfolio(_admin=Depends(require_admin)):
    return list_portfolio()


@router.post("/v1/admin/portfolio", response_model=PortfolioOut, status_code=201)
def admin_create_portfolio(payload: PortfolioWrite, _admin=Depends(require_admin)):
    row = {
        "id": str(uuid4()),
        "title": payload.title.strip(),
        "category": payload.category.value,
        "media_type": payload.media_type.value,
        "media_url": payload.media_url.strip(),
        "video_url": payload.video_url,
        "instagram_url": payload.instagram_url,
        "testimonial_text": payload.testimonial_text,
        "display_order": payload.display_order,
    }
    db = get_supabase()
    if db:
        res = db.table("portfolio_items").insert(row).execute()
        if res.data:
            store.log_activity("gallery", f"Added gallery item “{row['title']}”", {"id": row["id"]})
            return _map_item(res.data[0])
    store.LOCAL_PORTFOLIO.append(row)
    store.log_activity("gallery", f"Added gallery item “{row['title']}”", {"id": row["id"]})
    return _map_item(row)


@router.put("/v1/admin/portfolio/{item_id}", response_model=PortfolioOut)
def admin_update_portfolio(item_id: str, payload: PortfolioWrite, _admin=Depends(require_admin)):
    patch = {
        "title": payload.title.strip(),
        "category": payload.category.value,
        "media_type": payload.media_type.value,
        "media_url": payload.media_url.strip(),
        "video_url": payload.video_url,
        "instagram_url": payload.instagram_url,
        "testimonial_text": payload.testimonial_text,
        "display_order": payload.display_order,
    }
    db = get_supabase()
    if db:
        res = db.table("portfolio_items").update(patch).eq("id", item_id).execute()
        if res.data:
            store.log_activity("gallery", f"Updated gallery item “{patch['title']}”", {"id": item_id})
            return _map_item(res.data[0])
        raise HTTPException(status_code=404, detail="Item not found")
    for item in store.LOCAL_PORTFOLIO:
        if str(item.get("id")) == item_id:
            item.update(patch)
            store.log_activity("gallery", f"Updated gallery item “{patch['title']}”", {"id": item_id})
            return _map_item(item)
    raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/v1/admin/portfolio/{item_id}", status_code=204)
def admin_delete_portfolio(item_id: str, _admin=Depends(require_admin)):
    db = get_supabase()
    if db:
        db.table("portfolio_items").delete().eq("id", item_id).execute()
        store.log_activity("gallery", "Deleted gallery item", {"id": item_id})
        return Response(status_code=204)
    before = len(store.LOCAL_PORTFOLIO)
    store.LOCAL_PORTFOLIO[:] = [i for i in store.LOCAL_PORTFOLIO if str(i.get("id")) != item_id]
    if len(store.LOCAL_PORTFOLIO) == before:
        raise HTTPException(status_code=404, detail="Item not found")
    store.log_activity("gallery", "Deleted gallery item", {"id": item_id})
    return Response(status_code=204)
