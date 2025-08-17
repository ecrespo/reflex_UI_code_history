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
import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from openai import OpenAI

try:
    from zoneinfo import ZoneInfo  # Python 3.9+
except Exception:  # pragma: no cover
    ZoneInfo = None  # type: ignore

from reflex_UI_code_history.database import db_session, Efemerides, init_db


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    OPENAI_API_KEY: str | None = None
    OPENAI_MODEL: str = "gpt-4o-mini"


settings = Settings()


@dataclass
class GenerationResult:
    text: str
    historical_year: Optional[int]


SYSTEM_PROMPT = (
    "Eres un asistente especializado en efemérides históricas en español. "
    "Debes responder con UNA sola efeméride breve y verificable para la fecha indicada, "
    "con tono informativo y sin adornos innecesarios. Formato sugerido: "
    "'En {ANIO}, {hecho}.'. Si no hay un año claramente asociado, omite el año."
)

USER_PROMPT_TEMPLATE = (
    "Genera una efeméride concisa y en español para el día {day} de {month_name} (cualquier año histórico). "
    "Responde en una sola oración. Evita listas, comillas y markdown."
)

MONTHS_ES = [
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
]


def _local_today() -> datetime:
    tz_env = os.getenv("TZ")
    if tz_env and ZoneInfo is not None:
        tz = ZoneInfo(tz_env)
        return datetime.now(tz)
    # fallback: hora local del sistema
    return datetime.now().astimezone()


def _extract_historical_year(text: str) -> Optional[int]:
    # Busca un año entre 500 y 2100, priorizando 4 dígitos completos
    match = re.search(r"(?<!\d)(1[0-9]{3}|20[0-9]{2}|5[0-9]{2}|6[0-9]{2}|7[0-9]{2}|8[0-9]{2}|9[0-9]{2})(?!\d)", text)
    if match:
        try:
            year = int(match.group(0))
            # Filtra años improbables como 500-699 si no deseas incluirlos; aquí permitimos >= 700
            if year >= 700 and year <= 2100:
                return year
        except ValueError:
            pass
    return None


def _openai_chat_completion(prompt: str) -> Optional[str]:
    api_key = settings.OPENAI_API_KEY
    if not api_key:
        return None

    try:
        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=180,
        )
        if resp and resp.choices:
            content = resp.choices[0].message.content
            if isinstance(content, str) and content.strip():
                return content.strip()
    except Exception:
        return None

    return None


def generate_efemeride_text(day: int, month: int) -> GenerationResult:
    month_name = MONTHS_ES[month - 1]
    user_prompt = USER_PROMPT_TEMPLATE.format(day=day, month_name=month_name)

    text = _openai_chat_completion(user_prompt)

    if not text:
        # Fallback básico si no hay API: mantenemos el flujo pero marcamos claramente el origen
        text = (
            f"Efeméride generada automáticamente para el {day} de {month_name}. "
            f"(Configura OPENAI_API_KEY para generar contenido histórico real.)"
        )

    hist_year = _extract_historical_year(text)
    return GenerationResult(text=text, historical_year=hist_year)


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
