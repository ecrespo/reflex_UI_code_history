from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


def _default_sqlite_url() -> str:
    # Create a default SQLite database in the project root directory
    # two levels up from this file (project root)
    project_root = Path(__file__).resolve().parents[2]
    db_path = project_root / "app.db"
    # Use sqlite absolute file path
    return f"sqlite:///{db_path.as_posix()}"


@dataclass(frozen=True)
class DBConfig:
    """Configuration holder for database connectivity.

    Values are read from environment variables with sensible defaults.

    - DATABASE_URL: full SQLAlchemy URL (e.g., sqlite:////abs/path/app.db,
      postgresql+psycopg://user:pass@host:port/dbname, etc.)
    - SQL_ECHO: "1" or "true" to enable SQL echoing
    - POOL_PRE_PING: pre-ping connections ("1"/"true")
    - POOL_SIZE: integer
    - MAX_OVERFLOW: integer
    - POOL_RECYCLE: integer seconds
    """

    url: str
    echo: bool = False
    pool_pre_ping: bool = True
    pool_size: Optional[int] = None
    max_overflow: Optional[int] = None
    pool_recycle: Optional[int] = None

    @staticmethod
    def from_env() -> "DBConfig":
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
