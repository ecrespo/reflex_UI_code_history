#!/usr/bin/env python3
from __future__ import annotations

import sys
from datetime import date

# Reuse the existing ORM and DB session from the app
from reflex_UI_code_history.database import db_session, Efemerides, init_db


def main() -> int:
    """
    Inserta una efeméride de ejemplo para el día de hoy (17 de agosto) en app.db.

    - Usa la configuración por defecto (app.db en la raíz del proyecto).
    - Es idempotente: si ya existe una efeméride con display_date == hoy,
      no insertará un duplicado.
    """
    # Asegura que las tablas existen (idempotente)
    init_db()

    hoy = date.today()

    # Mensaje de ejemplo (ajustado al día 17 de agosto)
    ejemplo_evento = (
        "Efeméride de ejemplo: Un 17 de agosto se conmemoran diversos hechos históricos."
    )

    with db_session() as session:
        # Verificación idempotente: evitamos duplicados para la fecha exacta de hoy
        existente = (
            session.query(Efemerides)
            .filter(Efemerides.display_date == hoy)
            .first()
        )
        if existente:
            print(
                f"Ya existe una efeméride para la fecha {hoy.isoformat()} (id={existente.id})."
            )
            return 0

        fila = Efemerides(
            day=17,
            month=8,
            year=hoy.year,
            event=ejemplo_evento,
            display_date=hoy,
            historical_day=17,
            historical_month=8,
            historical_year=None,
        )
        session.add(fila)
        # commit se realiza automáticamente por el context manager en db_session

        print(
            f"Efeméride insertada para {hoy.isoformat()} (17 de agosto): '{ejemplo_evento}'"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
