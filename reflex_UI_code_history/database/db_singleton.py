from __future__ import annotations

import threading
from contextlib import contextmanager
from typing import Generator, Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from .config import DBConfig


class _Singleton(type):
    _instances: dict[type, object] = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):  # type: ignore[override]
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class DatabaseSingleton(metaclass=_Singleton):
    """Thread-safe Singleton managing SQLAlchemy engine and sessions.

    It can be used as a context manager to provide a Session:

        from reflex_UI_code_history.database import db
        with db as session:
            session.execute(...)
    """

    def __init__(self, config: Optional[DBConfig] = None) -> None:
        self._config = config or DBConfig.from_env()
        self._engine: Optional[Engine] = None
        self._SessionFactory: Optional[sessionmaker] = None
        self._ctx_session: Optional[Session] = None
        self._init_lock = threading.Lock()

    @property
    def config(self) -> DBConfig:
        return self._config

    @property
    def engine(self) -> Engine:
        if self._engine is None:
            with self._init_lock:
                if self._engine is None:
                    kwargs = {
                        "echo": self._config.echo,
                        "pool_pre_ping": self._config.pool_pre_ping,
                    }
                    if self._config.pool_size is not None:
                        kwargs["pool_size"] = self._config.pool_size
                    if self._config.max_overflow is not None:
                        kwargs["max_overflow"] = self._config.max_overflow
                    if self._config.pool_recycle is not None:
                        kwargs["pool_recycle"] = self._config.pool_recycle

                    # For SQLite file-based DBs, ensure check_same_thread=False for multi-threaded use
                    if self._config.url.startswith("sqlite:") and \
                       not self._config.url.startswith("sqlite+pysqlite:///"):
                        # SQLAlchemy 2.0 uses pysqlite by default; we keep generic URL.
                        pass

                    self._engine = create_engine(self._config.url, **kwargs)
        return self._engine  # type: ignore[return-value]

    @property
    def Session(self) -> sessionmaker:
        if self._SessionFactory is None:
            with self._init_lock:
                if self._SessionFactory is None:
                    self._SessionFactory = sessionmaker(bind=self.engine, class_=Session, autoflush=False, autocommit=False)
        return self._SessionFactory

    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        """Provide a transactional scope around a series of operations."""
        session: Session = self.Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    # Context manager protocol on the singleton itself
    def __enter__(self) -> Session:
        if self._ctx_session is not None:
            return self._ctx_session
        self._ctx_session = self.Session()
        return self._ctx_session

    def __exit__(self, exc_type, exc, tb) -> None:
        if self._ctx_session is None:
            return
        try:
            if exc is None:
                self._ctx_session.commit()
            else:
                self._ctx_session.rollback()
        finally:
            self._ctx_session.close()
            self._ctx_session = None


# Module-level singleton instance and helpers
_db_singleton = DatabaseSingleton()

db: DatabaseSingleton = _db_singleton


@contextmanager
def db_session() -> Generator[Session, None, None]:
    """Convenience context manager to get a session from the singleton."""
    with _db_singleton.session() as s:
        yield s
