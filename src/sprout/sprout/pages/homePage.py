"""
This file contians home page component.
"""

import reflex as rx

def homePage() -> rx.Component:
    """
    Simple and minimalistic home page component with a welcome message.

    :return: Home page component
    :rtype: rx.Component
    """
    return rx.text("Welcome to SPROUT!!!"),