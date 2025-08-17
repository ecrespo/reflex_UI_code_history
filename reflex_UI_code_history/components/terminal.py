import reflex as rx
from reflex_UI_code_history.styles.terminal_css import TERMINAL_BOX_STYLE


def terminal_box(*children: rx.Component, **props) -> rx.Component:
    """Caja con estilo de terminal minimalista."""
    return rx.box(
        *children,
        **TERMINAL_BOX_STYLE,
        **props,
    )


def typewriter_line(
    text: str,
    *,
    speed_ms: int = 30,
    start_delay_ms: int = 200,
    color: str = "#00ff88",
    line_height: str = "1.6",
    margin_bottom: str = "10px",
    id_: str | None = None,
) -> rx.Component:
    """Renderiza una línea con efecto de máquina de escribir (typewriter).

    Args:
        text: Texto a escribir progresivamente.
        speed_ms: Milisegundos entre cada carácter.
        start_delay_ms: Retraso inicial antes de comenzar la animación.
        color: Color del texto.
        line_height: Altura de línea CSS.
        margin_bottom: Margen inferior CSS.
        id_: Id opcional del elemento; si no se proporciona se genera uno estable basado en el hash del texto.
    """
    # Generar un id estable por texto para evitar colisiones simples.
    el_id = id_ or f"typew-{abs(hash(text)) % 10**8}"

    # Nota: usamos rx.script para ejecutar una animación sencilla en el cliente.
    script_code = f"""
(function(){{
  const text = {text!r};
  const elId = {el_id!r};
  function start(){{
    const el = document.getElementById(elId);
    if(!el) return; // si aún no está en el DOM, no hacemos nada
    el.textContent = '';
    let i = 0;
    function tick(){{
      if(i < text.length){{
        el.textContent = text.slice(0, ++i);
        setTimeout(tick, {speed_ms});
      }}
    }}
    setTimeout(tick, {start_delay_ms});
  }}
  // Iniciar cuando el navegador esté listo
  if(document.readyState === 'loading'){{
    document.addEventListener('DOMContentLoaded', start);
  }} else {{
    start();
  }}
}})();
"""

    return rx.fragment(
        rx.text(
            "",
            id=el_id,
            color=color,
            line_height=line_height,
            margin_bottom=margin_bottom,
        ),
        rx.script(script_code),
    )
