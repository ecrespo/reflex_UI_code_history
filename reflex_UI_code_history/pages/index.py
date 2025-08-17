"""Página principal (index) de la app de efemérides.

Se apoya en:
- components.terminal.terminal_box para el contenedor tipo terminal.
- styles.index_css para constantes de estilos y colores.
"""
from __future__ import annotations

import datetime as _dt
import urllib.parse as _url
import reflex as rx

from reflex_UI_code_history.components.terminal import terminal_box, typewriter_line
from reflex_UI_code_history.components.footer import footer
from reflex_UI_code_history.styles.index_css import (
    PROMPT_COLOR,
    DIM_COLOR,
    PAGE_CONTAINER_STYLE,
    BACKGROUND_BASE_STYLE,
    GREEN_BLOB_STYLE,
    BLUE_BLOB_STYLE,
    TERMINAL_CONTAINER_STYLE,
)



# Lista de efemérides (puedes ampliar libremente esta lista)
_EFEMERIDES: list[str] = [
    "1991: Linus Torvalds anuncia su proyecto personal que más tarde se convertirá en el kernel Linux.",
    "2001: Se lanza Mac OS X 10.0, marcando una nueva era para el sistema operativo de Apple basado en UNIX.",
    "1972: Se publica el lenguaje de programación C por Dennis Ritchie en los laboratorios Bell.",
    "1995: Se libera Java 1.0 por Sun Microsystems, popularizando el lema 'Write once, run anywhere'.",
    "2004: Se lanza Mozilla Firefox 1.0, impulsando estándares web abiertos y alternativas a IE.",
    "1989: Tim Berners-Lee propone la World Wide Web en el CERN, sentando las bases de la web moderna.",
    "2008: Google presenta Android, sistema operativo móvil basado en Linux y de código abierto.",
    "2012: GitHub alcanza 2 millones de repositorios públicos, consolidando el auge del desarrollo colaborativo.",
    "1976: Se funda Apple Computer por Steve Jobs, Steve Wozniak y Ronald Wayne.",
    "2009: Nace Bitcoin con el bloque génesis minado por Satoshi Nakamoto, iniciando la era blockchain.",
]


def _fact_of_today(today: _dt.date | None = None) -> str:
    """Obtiene la efeméride del día basándose en la fecha.

    Si no existe una efeméride específica para el día, se selecciona de manera
    determinista usando el día del año.
    """
    if today is None:
        today = _dt.date.today()
    day_of_year = int(today.strftime("%j"))  # Día del año (1-366)
    idx = (day_of_year - 1) % len(_EFEMERIDES)
    return _EFEMERIDES[idx]


def _format_date_es(today: _dt.date | None = None) -> str:
    if today is None:
        today = _dt.date.today()
    return today.strftime("%Y-%m-%d")


def index() -> rx.Component:
    today = _dt.date.today()
    fecha = _format_date_es(today)
    fact = _fact_of_today(today)

    # Construir URL de compartir en X (antes Twitter)
    base_url = "https://x.com/intent/tweet"
    share_text = f"Hoy ({fecha}): {fact}"
    share_link = "https://codehistory.seraph.to"
    share_qs = _url.urlencode({"text": share_text, "url": share_link})
    share_url = f"{base_url}?{share_qs}"

    return rx.flex(
        # Script para actualizar la hora del encabezado cada segundo en el cliente
        rx.script(
            """
(function(){
 function pad(n){return n.toString().padStart(2,'0');}
 function tick(){
  const d=new Date();
  const s=pad(d.getHours())+':'+pad(d.getMinutes())+':'+pad(d.getSeconds());
  const el=document.getElementById('clock');
  if(el) el.textContent=s;
 }
 tick();
 setInterval(tick,1000);
})();
"""
        ),
        # Capa base con degradado muy sutil
        rx.box(
            **BACKGROUND_BASE_STYLE,
        ),
        # Encabezado tipo prompt de terminal con hora en tiempo real
        rx.box(
            rx.flex(
                rx.text(
                    "code-history v0.0.1",
                    color=PROMPT_COLOR,
                    weight="bold",
                    size="3",
                ),
                rx.spacer(),
                rx.text("", id="clock", color=PROMPT_COLOR, size="3"),
                align="center",
                width="100%",
            ),
            bg="#0b0f10",
            color="#d1ffdb",
            border="1px solid #00ff88",
            border_radius="10px",
            padding="10px 14px",
            box_shadow="0 0 20px rgba(0,255,136,0.1)",
            font_family=(
                "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace"
            ),
            z_index=2,
            width=["92%", "700px"],
            margin_top="20px",
            margin_bottom="20px",
        ),
        # Blob verde principal (marca)
        rx.box(
            **GREEN_BLOB_STYLE,
        ),
        # Blob azulado complementario
        rx.box(
            **BLUE_BLOB_STYLE,
        ),
        # Contenido principal por encima del fondo: centrado y expansible
        rx.center(
            terminal_box(
                rx.text("reflex@efemerides:~$", color=PROMPT_COLOR, weight="bold", size="3"),
                rx.text("cat efemeride.txt", margin_top="2px", margin_bottom="10px", size="3"),
                rx.box(height="1px", bg=PROMPT_COLOR, opacity=0.25, margin_y="8px"),
                rx.flex(
                    rx.text("Hoy:", color=DIM_COLOR, margin_right="8px"),
                    rx.text(fecha, color="#ffffff"),
                    wrap="wrap",
                    gap="2",
                    align="center",
                    margin_bottom="8px",
                ),
                typewriter_line(f"• {fact}"),
                rx.text("Vuelve mañana para otra efeméride.", color=DIM_COLOR, size="2"),
                rx.flex(
                    rx.spacer(),
                    rx.button(
                        rx.hstack(
                            rx.text("𝕏", weight="bold", size="3"),
                            rx.text("Compartir", size="3"),
                            align="center",
                            gap="2",
                        ),
                        variant="soft",
                        color_scheme="grass",
                        size="3",
                        on_click=rx.call_script(
                            "window.open('" + share_url + "', '_blank', 'width=550,height=420');"
                        ),
                    ),
                    width="100%",
                    align="center",
                    margin_top="10px",
                ),
                **TERMINAL_CONTAINER_STYLE,
            ),
            flex="1",
            z_index=1,
            width="100%",
        ),
        # Footer al final de la página
        footer(),
        direction="column",
        align="center",
        **PAGE_CONTAINER_STYLE,
    )
