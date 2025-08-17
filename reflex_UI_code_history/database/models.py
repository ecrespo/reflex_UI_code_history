from __future__ import annotations

from typing import Optional

from sqlalchemy import Date, DateTime, Integer, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Efemerides(Base):
    """
    Tabla de efemérides.

    Requisitos de columnas según la solicitud:
    - day int4
    - month int4
    - year int4
    - event text
    - id int4
    - created_at timestampz
    - updated_at timestampz
    - display_date date
    - historical_day int4
    - historical_month int4
    - historical_year int4

    Notas:
    - En SQLite, Integer mapea a INTEGER; "timestampz" (con zona horaria) se modela
      como DateTime(timezone=True) a nivel SQLAlchemy; SQLite no aplica zonas de
      horario de forma nativa pero se mantiene la semántica a nivel ORM.
    - Se define "id" como clave primaria autoincremental por convención.
    """

    __tablename__ = "efemerides"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    day: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    month: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    event: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[Optional[str]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=True
    )
    updated_at: Mapped[Optional[str]] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=True
    )

    display_date: Mapped[Optional[str]] = mapped_column(Date, nullable=True)

    historical_day: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    historical_month: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    historical_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)


__all__ = ["Base", "Efemerides"]
