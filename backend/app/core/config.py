from functools import lru_cache

from pydantic import EmailStr, Field, SecretStr, field_validator, model_validator
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(default="HotelSec PolicyForge AI", alias="APP_NAME")
    app_version: str = Field(default="0.4.0", alias="APP_VERSION")
    app_env: str = Field(default="development", alias="APP_ENV")
    api_v1_prefix: str = "/api/v1"

    frontend_url: str = Field(default="http://localhost:5173", alias="APP_URL")
    cors_origins_raw: str = Field(
        default="http://localhost:5173,http://localhost:3000",
        alias="CORS_ORIGINS",
    )

    database_url: str = Field(
        default="postgresql+psycopg://hotelsec:change_me@localhost:5432/hotelsec",
        alias="DATABASE_URL",
    )

    jwt_secret_key: str = Field(
        default="change_me_with_a_long_random_secret",
        alias="JWT_SECRET_KEY",
    )
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=60, ge=5, le=1440,
        alias="ACCESS_TOKEN_EXPIRE_MINUTES",
    )

    ai_provider: str = Field(default="openai", alias="AI_PROVIDER")
    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o-mini", alias="OPENAI_MODEL")

    reports_dir: str = Field(default="reports/generated", alias="REPORTS_DIR")
    cookie_secure: bool = Field(default=False, alias="COOKIE_SECURE")
    ai_requests_per_hour: int = Field(default=20, ge=1, le=500, alias="AI_REQUESTS_PER_HOUR")
    ai_global_daily_limit: int = Field(default=50, ge=0, le=5000, alias="AI_GLOBAL_DAILY_LIMIT")
    smtp_host: str = Field(default="", alias="SMTP_HOST")
    smtp_port: int = Field(default=587, ge=1, le=65535, alias="SMTP_PORT")
    smtp_mode: Literal["starttls", "ssl"] = Field(default="starttls", alias="SMTP_MODE")
    smtp_username: str = Field(default="", alias="SMTP_USERNAME")
    smtp_password: SecretStr | None = Field(default=None, alias="SMTP_PASSWORD")
    smtp_from: EmailStr | None = Field(default=None, alias="SMTP_FROM")

    @field_validator("smtp_from", "smtp_password", mode="before")
    @classmethod
    def blank_mail_setting(cls, value):
        return None if value == "" else value

    @property
    def email_delivery_configured(self) -> bool:
        return bool(self.smtp_host and self.smtp_from)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        hide_input_in_errors=True,
    )

    @property
    def cors_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins_raw.split(",")
            if origin.strip()
        ]

    @model_validator(mode="after")
    def production_requires_https(self):
        if bool(self.smtp_username) != bool(self.smtp_password):
            raise ValueError("SMTP username and password must be configured together.")
        if any(character in self.smtp_host for character in ("\r", "\n", "/", "@")):
            raise ValueError("SMTP_HOST must be a hostname, not a URL or credentials.")
        if self.app_env == "production":
            if not self.cookie_secure or not self.frontend_url.startswith("https://"):
                raise ValueError("Production requires HTTPS APP_URL and COOKIE_SECURE=true.")
            if any(not origin.startswith("https://") for origin in self.cors_origins):
                raise ValueError("Production CORS origins must use HTTPS.")
            if any(marker in self.database_url for marker in ("change_me", "replace_with")):
                raise ValueError("Production requires a private database password.")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
