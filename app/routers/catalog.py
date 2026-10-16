from uuid import uuid4
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, Request, Response, UploadFile

from app.auth import normalize_phone, rate_limit_leads, require_admin
from app.schemas.models import CatalogRequestCreate, ProductOut, ProductWrite
from app import store

router = APIRouter(tags=["catalog"])

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_IMAGE_BYTES = 5 * 1024 * 1024

def _media_dir() -> Path:
    repo_root = Path(__file__).resolve().parent.parent.parent.parent.parent
    dest = repo_root / "frontend" / "lilian-frontend" / "public" / "media" / "catalog"
    dest.mkdir(parents=True, exist_ok=True)
    return dest


def _safe_image_url(raw: str) -> str:
    url = raw.strip()
    if not url:
        return ""
    if url.startswith("/media/catalog/"):
        return url
    if url.startswith(("https://", "http://")):
        return url
    return ""


def _clean(payload: ProductWrite) -> dict:
    return {
        "name": payload.name.strip()[:200],
        "brand": payload.brand.strip()[:100],
        "category": (payload.category or "Face").strip()[:50] or "Face",
        "shade": payload.shade.strip()[:100],
        "barcode": "".join(ch for ch in payload.barcode if ch.isalnum())[:50],
        "quantity": max(0, min(int(payload.quantity), 100000)),
        "notes": payload.notes.strip()[:2000],
        "image_url": _safe_image_url(payload.image_url or ""),
    }


@router.get("/v1/catalog", response_model=list[ProductOut])
def list_catalog():
    return store.get_products()


@router.post("/v1/catalog/requests", status_code=201)
def create_request(payload: CatalogRequestCreate, request: Request):
    rate_limit_leads(request)
    phone = normalize_phone(payload.phone_number)
    row = {
        "id": str(uuid4()),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "full_name": payload.full_name.strip(),
        "phone_number": phone,
        "note": payload.note.strip(),
        "items": [item.model_dump() for item in payload.items],
        "status": "New",
    }
    store.LOCAL_REQUESTS.append(row)
    names = ", ".join(f"{i['name']} ×{i['quantity']}" for i in row["items"][:4])
    store.log_activity(
        "catalog",
        f"Product request from {row['full_name']}: {names}",
        {"id": row["id"]},
    )
    store.persist()
    return {"ok": True, "request": row}


@router.get("/v1/admin/catalog", response_model=list[ProductOut])
def admin_catalog(_admin=Depends(require_admin)):
    return store.get_products()


@router.post("/v1/admin/catalog", response_model=ProductOut, status_code=201)
def admin_create_product(payload: ProductWrite, _admin=Depends(require_admin)):
    row = {"id": str(uuid4()), **_clean(payload)}
    if row["barcode"]:
        for existing in store.LOCAL_PRODUCTS:
            if existing.get("barcode") and existing["barcode"] == row["barcode"]:
                raise HTTPException(status_code=409, detail="A product with this barcode already exists")
    store.LOCAL_PRODUCTS.append(row)
    store.log_activity("catalog", f"Recorded product “{row['name']}” (qty {row['quantity']})", {"id": row["id"]})
    store.persist()
    return row


@router.put("/v1/admin/catalog/{product_id}", response_model=ProductOut)
def admin_update_product(product_id: str, payload: ProductWrite, _admin=Depends(require_admin)):
    patch = _clean(payload)
    for item in store.LOCAL_PRODUCTS:
        if str(item.get("id")) == product_id:
            if patch["barcode"]:
                for other in store.LOCAL_PRODUCTS:
                    if other is not item and other.get("barcode") == patch["barcode"]:
                        raise HTTPException(status_code=409, detail="A product with this barcode already exists")
            item.update(patch)
            store.log_activity("catalog", f"Updated product “{patch['name']}”", {"id": product_id})
            store.persist()
            return item
    raise HTTPException(status_code=404, detail="Product not found")


@router.delete("/v1/admin/catalog/{product_id}", status_code=204)
def admin_delete_product(product_id: str, _admin=Depends(require_admin)):
    removed = None
    remaining = []
    for p in store.LOCAL_PRODUCTS:
        if str(p.get("id")) == product_id:
            removed = p
        else:
            remaining.append(p)
    if not removed:
        raise HTTPException(status_code=404, detail="Product not found")
    store.LOCAL_PRODUCTS[:] = remaining
    img = (removed.get("image_url") or "").strip()
    if img.startswith("/media/catalog/"):
        file_path = _media_dir() / img.split("/")[-1]
        if file_path.exists() and file_path.is_file():
            file_path.unlink(missing_ok=True)
    store.log_activity("catalog", f"Removed catalog product \u201c{removed.get('name', '')}\u201d", {"id": product_id})
    store.persist()
    return Response(status_code=204)


@router.post("/v1/admin/catalog/upload")
async def admin_upload_image(
    file: UploadFile = File(...),
    _admin=Depends(require_admin),
):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Only JPEG, PNG, and WebP images are accepted")
    data = await file.read()
    if len(data) > MAX_IMAGE_BYTES:
        raise HTTPException(status_code=400, detail="Image must be under 5 MB")
    ext = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}.get(file.content_type, ".jpg")
    name = f"{uuid4().hex[:12]}{ext}"
    dest = _media_dir() / name
    dest.write_bytes(data)
    url = f"/media/catalog/{name}"
    return {"url": url}


@router.get("/v1/admin/catalog/requests")
def admin_requests(_admin=Depends(require_admin)):
    return store.get_requests()
