"""
This is the root file for the application. It also contains routing and root components for pages.

:author: Lukas Katona
"""

import reflex as rx
from rxconfig import config

from .components.layout import layout
from .pages.homePage import homePage
from .pages.analyzePage import analyzePage
from .pages.optimizePage import optimizePage

@rx.page(route="/", title="Home")
def home() -> rx.Component:
    """
    Home page root component with routing configured.

    :return: homePage component wrapped in base layout
    :rtype: rx.Component
    """
    return layout(
        homePage(),
    )

@rx.page(route="/analyze", title="Analyze")
def analyze() -> rx.Component:
    """
    Analyze page root component with routing configured.

    :return: analyzePage component wrapped in base layout
    :rtype: rx.Component
    """
    return layout(
        analyzePage(),
    )

@rx.page(route="/optimize", title="Optimize")
def optimize() -> rx.Component:
    """
    Optimize page root component with routing configured.

    :return: optimizePage component wrapped in base layout
    :rtype: rx.Component
    """
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
