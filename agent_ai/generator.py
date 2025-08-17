from __future__ import annotations

import re
from typing import Optional

from openai import OpenAI

from .prompts import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE, MONTHS_ES
from .settings import settings
from .types import GenerationResult


def extract_historical_year(text: str) -> Optional[int]:
    """Extrae un año histórico razonable del texto (700-2100)."""
    match = re.search(r"(?<!\d)(1[0-9]{3}|20[0-9]{2}|7[0-9]{2}|8[0-9]{2}|9[0-9]{2})(?!\d)", text)
    if match:
        try:
            year = int(match.group(0))
            if 700 <= year <= 2100:
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
    """Genera el texto de una efeméride para (day, month) y devuelve GenerationResult."""
    month_name = MONTHS_ES[month - 1]
    user_prompt = USER_PROMPT_TEMPLATE.format(day=day, month_name=month_name)

    text = _openai_chat_completion(user_prompt)

    if not text:
        # Fallback claro si no hay API key o falla el request
        text = (
            f"Efeméride generada automáticamente para el {day} de {month_name}. "
            f"(Configura OPENAI_API_KEY para generar contenido histórico real.)"
        )

    hist_year = extract_historical_year(text)
    return GenerationResult(text=text, historical_year=hist_year)
