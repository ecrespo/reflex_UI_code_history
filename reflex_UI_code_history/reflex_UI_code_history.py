"""App de efemérides diarias de programación/tecnología con estética de terminal."""

import reflex as rx

# Importar la página desde el paquete pages
from reflex_UI_code_history.pages.index import index

# Inicialización mínima de la app y registro de la página
app = rx.App()
app.add_page(
    index,
    title="Efemérides Tech - Diario",
    description="Una efeméride de programación y tecnología cada día en una interfaz tipo terminal.",
)
