from typing import Any, Optional

from app.config import settings

_client: Any = None


def has_supabase() -> bool:
    return bool(settings.supabase_url and settings.supabase_service_role_key)


def get_supabase() -> Optional[Any]:
    global _client
    if not has_supabase():
        return None
    if _client is None:
        try:
            from supabase import create_client
        except ImportError as exc:
            raise RuntimeError(
                "supabase package not installed; unset SUPABASE_URL or pip install supabase"
            ) from exc
        _client = create_client(settings.supabase_url, settings.supabase_service_role_key)
    return _client
