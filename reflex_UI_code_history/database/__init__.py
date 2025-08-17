"""Database package.

Expose configuration and a Singleton-based SQLAlchemy connection helper
that can also be used as a Python context manager.

Usage examples:

from reflex_UI_code_history.database import db, DBConfig

# Access engine
engine = db.engine

# Get a session via context manager on the singleton
with db as session:
    session.execute(...)

# Or use dedicated session context manager
from reflex_UI_code_history.database import db_session
with db_session() as session:
    ...
"""
from __future__ import annotations

from .config import DBConfig
from .db_singleton import DatabaseSingleton, db, db_session
from .models import Base, Efemerides


def init_db() -> None:
    """Ensure database tables exist (idempotent)."""
    Base.metadata.create_all(db.engine)


# Ensure the required tables (including efemerides) exist upon package import.
# This keeps behavior minimal and automatic for the current app setup.
init_db()

__all__ = [
    "DBConfig",
    "DatabaseSingleton",
    "db",
    "db_session",
    "Base",
    "Efemerides",
    "init_db",
]
