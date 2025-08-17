"""Boot sequence component extracted from the index page.

Provides a terminal-styled sequence simulating an OS boot.
"""
from __future__ import annotations

import reflex as rx

from reflex_UI_code_history.styles.index_css import PROMPT_COLOR
from reflex_UI_code_history.components.terminal import terminal_box


def boot_sequence_box() -> rx.Component:
    """Render the boot sequence UI box.

    Steps shown:
    1) Iniciando sistema de efemérides de programación y tecnología...
    2) Conectando con la base de datos ...[OK]
    3) Cargando datos históricos ...[OK]
    4) Sistema listo. Descrube la historia de la programación, tecnología y emprendimiento tecnológico día a día...[OK]
    """
    ok = rx.text("[OK]", color=PROMPT_COLOR, as_="span")
    return terminal_box(
        rx.text("boot@system:~$", color=PROMPT_COLOR, weight="bold", size="3"),
        rx.text("init --start", margin_top="2px", margin_bottom="10px", size="3"),
        rx.box(height="1px", bg=PROMPT_COLOR, opacity=0.25, margin_y="8px"),
        rx.vstack(
            rx.text("1. Iniciando sistema de efemérides de programación y tecnología...", size="3"),
            rx.hstack(
                rx.text("2. Conectando con la base de datos ...", size="3"),
                ok,
                gap="2",
                align="center",
                wrap="wrap",
            ),
            rx.hstack(
                rx.text("3. Cargando datos históricos ...", size="3"),
                ok,
                gap="2",
                align="center",
                wrap="wrap",
            ),
            rx.hstack(
                rx.text(
                    "4. Sistema listo. Descrube la historia de la programación, tecnología y emprendimiento tecnológico día a día...",
                    size="3",
                ),
                ok,
                gap="2",
                align="center",
                wrap="wrap",
            ),
            align="start",
            spacing="2",
        ),
        width=["92%", "700px"],
    )
