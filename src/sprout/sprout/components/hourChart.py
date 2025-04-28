"""
This file contains simple column graph with statistics agregated by hour of the day.
"""

import reflex as rx

def hourChart(title: str, data: list[dict[str,int]]) -> rx.Component:
    """
    Column graph that displays data agregated by hour of the day.

    :param title: Name of the graph
    :type title: str
    :param data: Data to display
    :type data: list[dict[str,int]]
    :return: Hour chart component
    :rtype: rx.Component
    """
    return rx.card(
        rx.vstack(
            rx.heading(title, size="4"),
            rx.recharts.bar_chart(
                rx.recharts.bar(
                    data_key="count",
                    fill=rx.color("accent", 8),
                ),
                rx.recharts.x_axis(data_key="hour"),
                rx.recharts.y_axis(),
                data=data,
                width="100%",
                height=250,
            ),
            rx.text("Hodina"),
            align_items="center",
        ),
        size="3",
        width="100%",
    ),