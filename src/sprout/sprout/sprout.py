import reflex as rx
from rxconfig import config

from .components.layout import layout
from .pages.homePage import homePage
from .pages.analyzePage import analyzePage
from .pages.optimizePage import optimizePage

@rx.page(route="/", title="Home")
def home() -> rx.Component:
    return layout(
        homePage(),
    )

@rx.page(route="/analyze", title="Analyze")
def analyze() -> rx.Component:
    return layout(
        analyzePage(),
    )

@rx.page(route="/optimize", title="Optimize")
def optimize() -> rx.Component:
    return layout(
        optimizePage(),
    )

app = rx.App(
    theme=rx.theme(
        appearance="light",
        has_background=True,
        accent_color="green",
    )
)
