from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    environment: str = "development"  # development | production
    supabase_url: str = ""
    supabase_service_role_key: str = ""
    supabase_jwt_secret: str = ""
    # HS256 secret for studio admin JWTs (required in production)
    auth_jwt_secret: str = ""
    auth_jwt_hours: int = 72
    # After the first admin exists, allow more signups only when true
    auth_allow_signup: bool = False
    frontend_origin: str = "http://localhost:3000,http://127.0.0.1:3000"
    lead_rate_limit: int = 8
    lead_rate_window_seconds: int = 600
    auth_rate_limit: int = 12
    auth_rate_window_seconds: int = 600
    data_dir: str = "data"

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"

    def jwt_secret(self) -> str:
        if self.auth_jwt_secret:
            return self.auth_jwt_secret
        if self.is_production:
            raise RuntimeError("AUTH_JWT_SECRET must be set in production")
        # Local-only fallback so signup/login works out of the box
        return "dev-being-lillian-auth-secret-change-me"


settings = Settings()
