import reflex as rx

from .navbar import navbar
from .footer import footer

def layout(content: rx.Component) -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.box(content, padding="1em", flex="1"),
        footer(),
        height="100vh",
    )
