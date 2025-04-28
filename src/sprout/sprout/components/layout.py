"""
This file contains base layout of the web page.
"""

import reflex as rx

from .navbar import navbar
from .footer import footer

def layout(content: rx.Component) -> rx.Component:
    """
    Base layout with navbar, main content and footer.

    :param content: Component to display between navbar and footer
    :type content: rx.Component
    :return: Content wrapped in a layout
    :rtype: rx.Component
    """
    return rx.vstack(
        navbar(),
        rx.box(content, padding="1em", flex="1", width="70%"),
        footer(),
        padding_top="5em",
        min_height="100vh",
        align_items="center",
    )
