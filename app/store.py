"""Mutable local store used when Supabase is not configured — persisted under data/."""

from __future__ import annotations

import copy
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.config import settings
from app.seed import LOCAL_LEAD_EVENTS, LOCAL_LEADS, SEED_PORTFOLIO, SEED_POSTS

DEFAULT_SETTINGS: dict[str, Any] = {
    "site_name": "Being Lillian",
    "tagline": "Makeup artistry, brand consulting, and collaborations.",
    "hero_headline": "Beauty with intention",
    "accent_color": "#C9A88A",
    "paper_color": "#F7F4EF",
    "ink_color": "#2A2420",
    "whatsapp_number": "0000000000",
    "instagram_url": "https://www.instagram.com/lilianbeauty_studio",
    "show_whatsapp_fab": True,
    "show_journal": True,
    "show_portfolio": True,
    "show_book_cta": True,
    "default_theme": "system",
}


def _serialize(row: dict) -> dict:
    out = copy.deepcopy(row)
    for key, val in list(out.items()):
        if hasattr(val, "value"):
            out[key] = val.value
    return out


def _data_dir() -> Path:
    root = Path(__file__).resolve().parent.parent / settings.data_dir
    root.mkdir(parents=True, exist_ok=True)
    return root


def _store_path() -> Path:
    return _data_dir() / "content.json"


LOCAL_POSTS: list[dict] = [_serialize(p) for p in SEED_POSTS]
LOCAL_PORTFOLIO: list[dict] = [_serialize(i) for i in SEED_PORTFOLIO]
LOCAL_SETTINGS: dict[str, Any] = copy.deepcopy(DEFAULT_SETTINGS)
LOCAL_ACTIVITY: list[dict] = []


def persist() -> None:
    payload = {
        "posts": LOCAL_POSTS,
        "portfolio": LOCAL_PORTFOLIO,
        "settings": LOCAL_SETTINGS,
        "leads": LOCAL_LEADS,
        "lead_events": LOCAL_LEAD_EVENTS,
        "activity": LOCAL_ACTIVITY,
    }
    _store_path().write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")


def load_persisted() -> None:
    path = _store_path()
    if not path.exists():
        return
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return
    if isinstance(data.get("posts"), list) and data["posts"]:
        LOCAL_POSTS[:] = data["posts"]
    if isinstance(data.get("portfolio"), list) and data["portfolio"]:
        LOCAL_PORTFOLIO[:] = data["portfolio"]
    if isinstance(data.get("settings"), dict) and data["settings"]:
        LOCAL_SETTINGS.clear()
        LOCAL_SETTINGS.update({**DEFAULT_SETTINGS, **data["settings"]})
    if isinstance(data.get("leads"), list):
        LOCAL_LEADS[:] = data["leads"]
    if isinstance(data.get("lead_events"), list):
        LOCAL_LEAD_EVENTS[:] = data["lead_events"]
    if isinstance(data.get("activity"), list):
        LOCAL_ACTIVITY[:] = data["activity"]


def log_activity(kind: str, message: str, meta: dict | None = None) -> None:
    LOCAL_ACTIVITY.insert(
        0,
        {
            "id": f"act-{len(LOCAL_ACTIVITY) + 1}-{int(datetime.now(timezone.utc).timestamp())}",
            "at": datetime.now(timezone.utc).isoformat(),
            "kind": kind,
            "message": message,
            "meta": meta or {},
        },
    )
    del LOCAL_ACTIVITY[100:]
    persist()


def get_posts() -> list[dict]:
    return sorted(LOCAL_POSTS, key=lambda p: p.get("published_at", ""), reverse=True)


def get_portfolio() -> list[dict]:
    return sorted(LOCAL_PORTFOLIO, key=lambda i: int(i.get("display_order") or 0))


def get_settings() -> dict:
    return copy.deepcopy(LOCAL_SETTINGS)


def update_settings(patch: dict) -> dict:
    for key, val in patch.items():
        if key in LOCAL_SETTINGS and val is not None:
            LOCAL_SETTINGS[key] = val
    log_activity("settings", "Site appearance / capabilities updated", patch)
    return get_settings()


def activity_feed(limit: int = 40) -> list[dict]:
    events = list(LOCAL_ACTIVITY)
    for ev in LOCAL_LEAD_EVENTS[-20:]:
        events.append(
            {
                "id": f"lead-ev-{ev.get('lead_id')}",
                "at": datetime.now(timezone.utc).isoformat(),
                "kind": "lead",
                "message": str(ev.get("event") or "Lead updated"),
                "meta": {"lead_id": ev.get("lead_id")},
            }
        )
    events.sort(key=lambda e: e.get("at", ""), reverse=True)
    return events[:limit]


# Load once on import
load_persisted()
