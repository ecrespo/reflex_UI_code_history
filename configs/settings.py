from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

try:
    # pydantic-settings is optional for this project runtime, but present in scripts.
    from pydantic_settings import BaseSettings, SettingsConfigDict
except Exception:  # pragma: no cover
    BaseSettings = object  # type: ignore
    SettingsConfigDict = dict  # type: ignore


# --------- Helpers ---------

def _project_root() -> Path:
    # Project root is the parent of this file's directory (configs/) relative to repo root
    return Path(__file__).resolve().parents[1]


def _default_sqlite_url() -> str:
    db_path = _project_root() / "app.db"
    return f"sqlite:///{db_path.as_posix()}"


# --------- Central App Settings ---------

class AppSettings(BaseSettings):
    """Central application settings loaded from environment/.env.

    This class collects configuration variables used across the app and scripts.
    It loads from .env by default when pydantic-settings is available.
    """

    try:
        model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")  # type: ignore
    except Exception:  # pragma: no cover
        # If pydantic-settings isn't available at runtime, ignore .env loading.
        pass

    # Database
    DATABASE_URL: Optional[str] = None
    SQL_ECHO: Optional[str] = None
    POOL_PRE_PING: Optional[str] = None
    POOL_SIZE: Optional[int] = None
    MAX_OVERFLOW: Optional[int] = None
    POOL_RECYCLE: Optional[int] = None

    # OpenAI / AI generation (used by scripts)
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"

    # Misc
    TZ: Optional[str] = None


# Singleton-ish instance to be reused
app_settings = AppSettings() if isinstance(AppSettings, type) else None  # type: ignore


# --------- DB Config (used by SQLAlchemy) ---------

@dataclass(frozen=True)
class DBConfig:
    """Configuration holder for database connectivity.

    Values are read from environment variables (or AppSettings) with sensible defaults.
    """

    url: str
    echo: bool = False
    pool_pre_ping: bool = True
    pool_size: Optional[int] = None
    max_overflow: Optional[int] = None
    pool_recycle: Optional[int] = None

    @staticmethod
    def from_env() -> "DBConfig":
        """Build DBConfig from OS environment variables.

        Keeps compatibility with existing code paths.
        """
        url = os.getenv("DATABASE_URL") or _default_sqlite_url()
        echo = (os.getenv("SQL_ECHO", "0").lower() in {"1", "true", "yes"})
        pool_pre_ping = (os.getenv("POOL_PRE_PING", "1").lower() in {"1", "true", "yes"})

        def _opt_int(var: str) -> Optional[int]:
            val = os.getenv(var)
            if val is None or val == "":
                return None
            try:
                return int(val)
            except ValueError:
                return None

        pool_size = _opt_int("POOL_SIZE")
        max_overflow = _opt_int("MAX_OVERFLOW")
        pool_recycle = _opt_int("POOL_RECYCLE")

        return DBConfig(
            url=url,
            echo=echo,
            pool_pre_ping=pool_pre_ping,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_recycle=pool_recycle,
        )

    @staticmethod
    def from_settings(settings: AppSettings | None = None) -> "DBConfig":
        """Build DBConfig from AppSettings instance (preferred central source)."""
        s = settings or app_settings
        # Fallback to env/defaults if settings is not available
        if s is None:
            return DBConfig.from_env()

        url = s.DATABASE_URL or _default_sqlite_url()
        echo = str(s.SQL_ECHO or "0").lower() in {"1", "true", "yes"}
        pool_pre_ping = str(s.POOL_PRE_PING or "1").lower() in {"1", "true", "yes"}
        pool_size = s.POOL_SIZE
        max_overflow = s.MAX_OVERFLOW
        pool_recycle = s.POOL_RECYCLE
        return DBConfig(
            url=url,
            echo=echo,
            pool_pre_ping=pool_pre_ping,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_recycle=pool_recycle,
        )
