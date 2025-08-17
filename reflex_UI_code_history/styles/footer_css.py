"""Estilos del componente Footer.

Este módulo centraliza los estilos usados por el componente
`components.footer.footer` para mantener una separación clara entre
presentación y estructura.
"""

# Estilos del contenedor principal del footer
FOOTER_CONTAINER_STYLE: dict = {
    "width": "100%",
    "justify": "center",
    "padding_bottom": "1rem",
    "z_index": 2,
}

# Estilos del texto del footer
FOOTER_TEXT_STYLE: dict = {
    "color": "#8affc1",
    "size": "2",
    "margin_top": "1rem",
}

# Estilos del enlace dentro del footer
FOOTER_LINK_STYLE: dict = {
    "color": "#00ff88",
    "_hover": {"text_decoration": "underline"},
}
