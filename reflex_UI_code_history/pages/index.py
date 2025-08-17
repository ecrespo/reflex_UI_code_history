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
from reflex_UI_code_history.database import db_session, Efemerides
from reflex_UI_code_history.components.footer import footer
from reflex_UI_code_history.components.boot_sequence import boot_sequence_box
from reflex_UI_code_history.styles.index_css import (
    PROMPT_COLOR,
    DIM_COLOR,
    PAGE_CONTAINER_STYLE,
    BACKGROUND_BASE_STYLE,
    GREEN_BLOB_STYLE,
    BLUE_BLOB_STYLE,
    TERMINAL_CONTAINER_STYLE,
)



def _fact_of_today(today: _dt.date | None = None) -> str:
    """Obtiene la efeméride del día desde la base de datos.

    Estrategia de búsqueda:
    1) Coincidencia exacta por display_date == hoy.
    2) Si no hay, intentar por day y month (ignorando el año), tomando la más reciente.
    3) Si no hay resultados, devolver un mensaje amigable.
    """
    if today is None:
        today = _dt.date.today()

    # Consulta a la base de datos usando el ORM
    with db_session() as session:
        # 1) Coincidencia exacta por display_date
        row = (
            session.query(Efemerides)
            .filter(Efemerides.display_date == today)
            .order_by(Efemerides.id.desc())
            .first()
        )
        if row and row.event:
            return row.event

        # 2) Fallback: por día y mes
        row_dm = (
            session.query(Efemerides)
            .filter(
                Efemerides.day == today.day,
                Efemerides.month == today.month,
            )
            .order_by(Efemerides.id.desc())
            .first()
        )
        if row_dm and row_dm.event:
            return row_dm.event

    # 3) Mensaje por defecto si no hay registros
    return "No hay efeméride registrada para hoy."


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
        # Componente de arranque (boot) inmediatamente después del header
        rx.center(
            boot_sequence_box(),
            z_index=1,
            width="100%",
        ),
        # Separador tipo <hr> verde
        rx.box(height="2px", bg=PROMPT_COLOR, opacity=0.6, width=["92%", "700px"], margin_y="12px", border_radius="2px"),
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
