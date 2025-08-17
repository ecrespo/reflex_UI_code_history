#!/usr/bin/env python3
from __future__ import annotations

"""
Script: generate_tomorrow_efemeride.py

Objetivo:
- Generar cada día la efeméride del día siguiente utilizando IA y guardarla en app.db.
- Garantizar que la fecha (display_date) corresponda estrictamente al día siguiente.
- Evitar duplicados (idempotencia) si ya existe una efeméride para esa fecha.

Uso previsto (cron):
- Ejecútalo una vez al día, por ejemplo a las 23:59 hora local.
  Ejemplo de crontab (Linux):
    59 23 * * * /usr/bin/env bash -lc 'cd /path/al/proyecto && ./generate_tomorrow_efemeride.py >> cron_efemerides.log 2>&1'

Variables de entorno (opcional, para IA real):
- OPENAI_API_KEY: se obtiene vía pydantic-settings desde el archivo .env.
- OPENAI_MODEL: (opcional) modelo a usar. Por defecto: gpt-4o-mini
- TZ: (opcional) zona horaria del sistema/usuario si tu programador de tareas no ajusta TZ.

Dependencias:
- Requiere "pydantic-settings" y "openai" para la generación con IA usando el SDK oficial de OpenAI.

Notas sobre los campos:
- display_date: se fija al día siguiente (fecha local) y es el campo de unicidad lógica.
- day, month, year: se rellenan con los componentes de display_date (el "día que se muestra").
- historical_*: si el modelo menciona un año histórico exacto (p.ej. 1945), intentamos extraerlo.

"""

import os
from datetime import datetime, timedelta
from typing import Optional

from agent_ai import generate_efemeride_text

try:
    from zoneinfo import ZoneInfo  # Python 3.9+
except Exception:  # pragma: no cover
    ZoneInfo = None  # type: ignore

from reflex_UI_code_history.database import db_session, Efemerides, init_db


def _local_today() -> datetime:
    tz_env = os.getenv("TZ")
    if tz_env and ZoneInfo is not None:
        tz = ZoneInfo(tz_env)
        return datetime.now(tz)
    # fallback: hora local del sistema
    return datetime.now().astimezone()


def ensure_tomorrow_efemeride() -> None:
    # Asegura tablas existentes
    init_db()

    now_local = _local_today()
    tomorrow = (now_local + timedelta(days=1)).date()

    with db_session() as session:
        existente = (
            session.query(Efemerides)
            .filter(Efemerides.display_date == tomorrow)
            .first()
        )
        if existente:
            print(
                f"Ya existe efeméride para {tomorrow.isoformat()} (id={existente.id}). No se crea otra."
            )
            return

        gen = generate_efemeride_text(tomorrow.day, tomorrow.month)

        fila = Efemerides(
            day=tomorrow.day,
            month=tomorrow.month,
            year=tomorrow.year,  # año de la fecha mostrada (no necesariamente el histórico)
            event=gen.text,
            display_date=tomorrow,
            historical_day=None,   # si se desea, podría intentar extraer el día del texto, pero suele no venir
            historical_month=None, # idem
            historical_year=gen.historical_year,
        )
        session.add(fila)
        # commit via context manager

        print(
            f"Efeméride creada para {tomorrow.isoformat()}: {gen.text}"
        )


def main() -> int:
    try:
        ensure_tomorrow_efemeride()
        return 0
    except Exception as e:
        # No dejamos stacktrace para ejecución por cron, salvo que se requiera
        print(f"Error al generar la efeméride: {e}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
