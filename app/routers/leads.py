from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Request

from app.auth import normalize_phone, rate_limit_leads, require_admin
from app.db import get_supabase, has_supabase
from app.schemas.models import LeadCreate, LeadOut, LeadStatus, LeadStatusUpdate
from app import store
from app.seed import LOCAL_LEAD_EVENTS, LOCAL_LEADS

router = APIRouter(tags=["leads"])


def _compose_notes(payload: LeadCreate) -> str | None:
    parts = []
    if payload.location:
        parts.append(f"Location: {payload.location}")
    if payload.budget:
        parts.append(f"Budget: {payload.budget}")
    if payload.notes:
        parts.append(payload.notes)
    return "\n".join(parts) if parts else None


@router.post("/v1/leads", status_code=201)
def create_lead(payload: LeadCreate, request: Request):
    rate_limit_leads(request)
    phone = normalize_phone(payload.phone_number)
    notes = _compose_notes(payload)
    row = {
        "full_name": payload.full_name.strip(),
        "phone_number": phone,
        "email": (payload.email or "").strip() or None,
        "service_type": payload.service_type.value,
        "event_date": payload.event_date.isoformat() if payload.event_date else None,
        "status": LeadStatus.New.value,
        "notes": notes,
    }
    db = get_supabase()
    if db:
        res = db.table("leads").insert(row).execute()
        data = res.data[0] if res.data else {**row, "id": str(uuid4()), "created_at": datetime.now(timezone.utc).isoformat()}
        return {"ok": True, "stored": "supabase", "lead": data}
    local = {**row, "id": str(uuid4()), "created_at": datetime.now(timezone.utc).isoformat()}
    LOCAL_LEADS.append(local)
    store.log_activity(
        "lead",
        f"New inquiry from {local['full_name']} ({local['service_type']})",
        {"id": local["id"]},
    )
    store.persist()
    return {"ok": True, "stored": "local", "lead": local}


@router.get("/v1/admin/leads", response_model=list[LeadOut])
def list_leads(_admin=Depends(require_admin)):
    db = get_supabase()
    if db:
        res = db.table("leads").select("*").order("created_at", desc=True).execute()
        return res.data or []
    return sorted(LOCAL_LEADS, key=lambda x: x.get("created_at", ""), reverse=True)


@router.patch("/v1/admin/leads/{lead_id}")
def update_lead_status(lead_id: str, body: LeadStatusUpdate, admin=Depends(require_admin)):
    note_line = f"[{datetime.now(timezone.utc).isoformat()}] {admin.get('sub', 'admin')}: status → {body.status.value}"
    if body.note:
        note_line += f" — {body.note}"
    db = get_supabase()
    if db:
        existing = db.table("leads").select("*").eq("id", lead_id).limit(1).execute()
        if not existing.data:
            raise HTTPException(status_code=404, detail="Lead not found")
        prev = existing.data[0]
        notes = (prev.get("notes") or "")
        notes = f"{notes}\n{note_line}".strip() if notes else note_line
        updated = (
            db.table("leads")
            .update({"status": body.status.value, "notes": notes})
            .eq("id", lead_id)
            .execute()
        )
        LOCAL_LEAD_EVENTS.append({"lead_id": lead_id, "event": note_line})
        return updated.data[0] if updated.data else {"id": lead_id, "status": body.status.value, "notes": notes}
    for lead in LOCAL_LEADS:
        if str(lead.get("id")) == lead_id:
            lead["status"] = body.status.value
            lead["notes"] = f"{lead.get('notes') or ''}\n{note_line}".strip()
            LOCAL_LEAD_EVENTS.append({"lead_id": lead_id, "event": note_line})
            store.persist()
            return lead
    raise HTTPException(status_code=404, detail="Lead not found")
