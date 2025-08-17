from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class GenerationResult:
    text: str
    historical_year: Optional[int]
