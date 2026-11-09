"""All configuration comes from environment variables (or a .env file).

Every setting below can be overridden with an env var of the same name in
UPPER_CASE, e.g. LLM_PROVIDER=myvendor. See .env.example for the full list.
"""
from __future__ import annotations

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # --- App -----------------------------------------------------------------
    app_name: str = "collections-agent-backend"
    environment: str = "local"                  # local | staging | production
    api_key: str = "change-me"                  # sent by clients as the X-API-Key header
    public_base_url: str = "http://localhost:8000"  # used to build webhook URLs for providers
    lender_name: str = "Northbank"              # who the agent calls on behalf of
    log_level: str = "INFO"
    # Local testing only: pretend it is this time (ISO 8601, e.g. 2026-11-09T10:00:00Z)
    # so calling-hours rules don't block you in the evening. Refused in production.
    clock_override: str = ""

    # --- Storage -------------------------------------------------------------
    database_url: str = "sqlite:///./data/app.db"  # Postgres: postgresql+psycopg://user:pass@host:5432/db

    # --- Providers: each value is a name registered in app/providers --------
    stt_provider: str = "mock"          # speech-to-text
    llm_provider: str = "mock"          # conversation model
    tts_provider: str = "mock"          # text-to-speech
    voice_provider: str = "console"     # telephony (place calls, play audio, transfer)
    messaging_provider: str = "console" # SMS / WhatsApp / email
    crm_provider: str = "mock"          # lender's CRM
    payments_provider: str = "mock"     # payment links
    state_store: str = "database"       # where live call state is kept between turns

    # --- Provider credentials (only needed for real vendors) ----------------
    llm_model: str = ""
    llm_api_key: str = ""
    llm_timeout_seconds: float = 8.0
    stt_api_key: str = ""
    stt_min_confidence: float = 0.75    # below this we ask the customer to repeat
    tts_api_key: str = ""
    tts_voice: str = "default"
    voice_api_key: str = ""
    messaging_api_key: str = ""
    crm_base_url: str = ""
    crm_api_key: str = ""
    payments_api_key: str = ""

    # --- Worker ----------------------------------------------------------------
    worker_poll_seconds: int = 30
    max_concurrent_calls: int = 5
    call_timeout_minutes: int = 30      # in-progress calls older than this are closed as abandoned


@lru_cache
def get_settings() -> Settings:
    return Settings()
