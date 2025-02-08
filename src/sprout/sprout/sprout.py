import reflex as rx
from rxconfig import config

from .components.layout import layout
from .pages.homePage import home
from .pages.analyzePage import analyze
from .pages.optimizePage import optimize

@rx.page(route="/", title="Home")
def homePage() -> rx.Component:
    return layout(
        home(),
    )

@rx.page(route="/analyze", title="Analyze")
def analyzePage() -> rx.Component:
    return layout(
        analyze(),
    )

@rx.page(route="/optimize", title="Optimize")
def optimizePage() -> rx.Component:
    return layout(
        optimize(),
    )


app = rx.App(
    theme=rx.theme(
        appearance="light",
        has_background=True,
        accent_color="green",
    )
)
