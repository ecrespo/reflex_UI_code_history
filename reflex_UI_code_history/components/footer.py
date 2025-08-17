"""Footer component for the application."""

import reflex as rx
from reflex_UI_code_history.styles.footer_css import (
    FOOTER_CONTAINER_STYLE,
    FOOTER_TEXT_STYLE,
    FOOTER_LINK_STYLE,
)

def footer() -> rx.Component:
    """Create a footer with copyright information."""
    return rx.flex(
        rx.text(
            "© 2025 Seraph13 by ",
            rx.link(
                "Ernesto Crespo",
                href="https://www.seraph.to",
                **FOOTER_LINK_STYLE,
            ),
            **FOOTER_TEXT_STYLE,
        ),
        **FOOTER_CONTAINER_STYLE,
    )
