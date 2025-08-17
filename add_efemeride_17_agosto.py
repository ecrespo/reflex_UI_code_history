#!/usr/bin/env python3
from __future__ import annotations

"""
Script: add_efemeride_17_agosto.py

Objetivo:
- Insertar una efeméride para el 17 de agosto usando OpenAI de la misma forma que generate_tomorrow_efemeride.py.
- Mantener idempotencia: si ya existe una efeméride para el día de ejecución (display_date == hoy), no insertar duplicado.
- La efeméride generada debe estar enfocada en "17 de agosto" (cualquier año histórico), pero la fecha mostrada (display_date) será el día de ejecución.

Notas:
- Requiere variables de entorno vía .env: OPENAI_API_KEY (opcional), OPENAI_MODEL (opcional, por defecto gpt-4o-mini).
- Si no hay API key se usará un fallback claro.
"""

from datetime import date

from agent_ai import generate_efemeride_text

# Reuse ORM and DB session from the app
from reflex_UI_code_history.database import db_session, Efemerides, init_db



def main() -> int:
    """
    Inserta una efeméride para el 17 de agosto usando OpenAI (mismo flujo que generate_tomorrow_efemeride.py).

    - Usa la configuración por defecto (app.db en la raíz del proyecto).
    - Es idempotente: si ya existe una efeméride con display_date == hoy, no inserta duplicado.
    - Genera el texto específicamente sobre "17 de agosto".
    """
    # Asegura que las tablas existen (idempotente)
    init_db()

    hoy = date.today()

    gen = generate_efemeride_text(17, 8)

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
            event=gen.text,
            display_date=hoy,
            historical_day=None,
            historical_month=None,
            historical_year=gen.historical_year,
        )
        session.add(fila)
        # commit se realiza automáticamente por el context manager en db_session

        print(
            f"Efeméride insertada para {hoy.isoformat()} (17 de agosto): '{gen.text}'"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
