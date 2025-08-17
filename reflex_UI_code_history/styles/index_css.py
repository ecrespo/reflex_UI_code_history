"""Estilos y constantes de la página index."""

# Colores
PROMPT_COLOR = "#00ff88"
DIM_COLOR = "#8affc1"

# Contenedor principal (rx.center)
PAGE_CONTAINER_STYLE: dict = {
    "position": "relative",
    "overflow": "hidden",
    "bg": "#050708",
    "min_height": "100vh",
    "padding_y": "10vh",
}

# Fondo base (capa de degradado)
BACKGROUND_BASE_STYLE: dict = {
    "position": "absolute",
    "inset": "0",
    "bg": "linear-gradient(135deg, #050708 0%, #0a0d0f 100%)",
    "z_index": 0,
}

# Blob verde principal
GREEN_BLOB_STYLE: dict = {
    "position": "absolute",
    "top": ["-15%", "-10%"],
    "left": ["-20%", "-10%"],
    "width": ["90vw", "55vw"],
    "height": ["90vw", "55vw"],
    "bg": (
        "radial-gradient( circle at 30% 30%, rgba(0,255,136,0.28), rgba(0,255,136,0.0) 60%)"
    ),
    "filter": "blur(50px)",
    "opacity": 0.9,
    "animation": "none",
    "transform": "translateZ(0)",
    "z_index": 0,
}

# Blob azulado complementario
BLUE_BLOB_STYLE: dict = {
    "position": "absolute",
    "bottom": ["-20%", "-15%"],
    "right": ["-25%", "-15%"],
    "width": ["100vw", "60vw"],
    "height": ["100vw", "60vw"],
    "bg": (
        "radial-gradient( circle at 70% 70%, rgba(0,200,255,0.18), rgba(0,200,255,0.0) 60%)"
    ),
    "filter": "blur(55px)",
    "opacity": 0.9,
    "animation": "none",
    "transform": "translateZ(0)",
    "z_index": 0,
}

# Contenedor del terminal (ajustes de layout en index)
TERMINAL_CONTAINER_STYLE: dict = {
    "width": ["92%", "700px"],
    "position": "relative",
    "z_index": 1,
}
