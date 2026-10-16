from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Response

from app.auth import require_admin
from app.db import get_supabase
from app.schemas.models import PostOut, PostWrite
from app import store

router = APIRouter(tags=["posts"])


def _map_post(row: dict) -> dict:
    body = str(row.get("body_markdown") or "")
    quote = row.get("quote")
    if not quote:
        for line in body.splitlines():
            if line.startswith(">"):
                quote = line.lstrip("> ").strip()
                break
    excerpt = row.get("excerpt") or ""
    if not excerpt:
        plain = "\n".join(l for l in body.splitlines() if l and not l.startswith(">"))
        excerpt = plain.split("\n\n")[0][:220] if plain else ""
    return {
        "id": str(row.get("id")),
        "slug": row["slug"],
        "title": row["title"],
        "category": row["category"].value if hasattr(row["category"], "value") else row["category"],
        "published_at": str(row.get("published_at", ""))[:10],
        "body_markdown": body,
        "excerpt": excerpt,
        "quote": quote,
        "media_urls": row.get("media_urls") or [],
        "is_featured": bool(row.get("is_featured")),
    }


def _list_local() -> list[dict]:
    return [_map_post(p) for p in store.get_posts()]


@router.get("/v1/posts", response_model=list[PostOut])
def list_posts():
    db = get_supabase()
    if db:
        res = db.table("content_posts").select("*").order("published_at", desc=True).execute()
        if res.data:
            return [_map_post(r) for r in res.data]
    return _list_local()


@router.get("/v1/posts/{slug}", response_model=PostOut)
def get_post(slug: str):
    db = get_supabase()
    if db:
        res = db.table("content_posts").select("*").eq("slug", slug).limit(1).execute()
        if res.data:
            return _map_post(res.data[0])
    for post in store.get_posts():
        if post["slug"] == slug:
            return _map_post(post)
    raise HTTPException(status_code=404, detail="Post not found")


@router.get("/v1/admin/posts", response_model=list[PostOut])
def admin_list_posts(_admin=Depends(require_admin)):
    return list_posts()


@router.post("/v1/admin/posts", response_model=PostOut, status_code=201)
def admin_create_post(payload: PostWrite, _admin=Depends(require_admin)):
    row = {
        "id": str(uuid4()),
        "slug": payload.slug.strip().lower().replace(" ", "-"),
        "title": payload.title.strip(),
        "category": payload.category.value,
        "published_at": payload.published_at[:10],
        "body_markdown": payload.body_markdown,
        "excerpt": payload.excerpt,
        "quote": payload.quote,
        "media_urls": payload.media_urls,
        "is_featured": payload.is_featured,
    }
    db = get_supabase()
    if db:
        res = db.table("content_posts").insert(row).execute()
        if res.data:
            store.log_activity("journal", f"Created post “{row['title']}”", {"id": row["id"]})
            return _map_post(res.data[0])
    if any(p["slug"] == row["slug"] for p in store.LOCAL_POSTS):
        raise HTTPException(status_code=409, detail="Slug already exists")
    store.LOCAL_POSTS.append(row)
    store.log_activity("journal", f"Created post “{row['title']}”", {"id": row["id"]})
    store.persist()
    return _map_post(row)


@router.put("/v1/admin/posts/{post_id}", response_model=PostOut)
def admin_update_post(post_id: str, payload: PostWrite, _admin=Depends(require_admin)):
    patch = {
        "slug": payload.slug.strip().lower().replace(" ", "-"),
        "title": payload.title.strip(),
        "category": payload.category.value,
        "published_at": payload.published_at[:10],
        "body_markdown": payload.body_markdown,
        "excerpt": payload.excerpt,
        "quote": payload.quote,
        "media_urls": payload.media_urls,
        "is_featured": payload.is_featured,
    }
    db = get_supabase()
    if db:
        res = db.table("content_posts").update(patch).eq("id", post_id).execute()
        if res.data:
            store.log_activity("journal", f"Updated post “{patch['title']}”", {"id": post_id})
            return _map_post(res.data[0])
        raise HTTPException(status_code=404, detail="Post not found")
    for post in store.LOCAL_POSTS:
        if str(post.get("id")) == post_id:
            post.update(patch)
            store.log_activity("journal", f"Updated post “{patch['title']}”", {"id": post_id})
            return _map_post(post)
    raise HTTPException(status_code=404, detail="Post not found")


@router.delete("/v1/admin/posts/{post_id}", status_code=204)
def admin_delete_post(post_id: str, _admin=Depends(require_admin)):
    db = get_supabase()
    if db:
        db.table("content_posts").delete().eq("id", post_id).execute()
        store.log_activity("journal", "Deleted journal post", {"id": post_id})
        return Response(status_code=204)
    before = len(store.LOCAL_POSTS)
    store.LOCAL_POSTS[:] = [p for p in store.LOCAL_POSTS if str(p.get("id")) != post_id]
    if len(store.LOCAL_POSTS) == before:
        raise HTTPException(status_code=404, detail="Post not found")
    store.log_activity("journal", "Deleted journal post", {"id": post_id})
    return Response(status_code=204)
