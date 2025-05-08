"""
This file contains card component for displaying simple information.

:author: Lukas Katona
"""

import reflex as rx

def infoCard(title: str, info: str, loading = False) -> rx.Component:
    """
    Card displaying simple information.

    :param title: Name of displayed information
    :type title: str
    :param info: Value of displayed information
    :type info: str
    :param loading: displays loading indicator if True, defaults to False
    :type loading: bool, optional
    :return: Info card component
    :rtype: rx.Component
    """
    return rx.card(
        rx.vstack(
            rx.heading(title, size="4"),
            rx.cond(
                loading,
                rx.spinner(size="3"),
                rx.heading(info, size="8"),
            ),
            align_items="center",
            justify="between",
            height="100%",
        ),
        size="3",
        width="100%",
    ),
