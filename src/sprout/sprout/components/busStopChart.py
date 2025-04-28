"""
This files contains bus stop chart component
"""

import reflex as rx

def busStopChart(title: str, data: list[dict[str,int]], max: int, numOfEntries: int, leftMargin: int) -> rx.Component:
    """
    Component that displays bus stops on one axis and average load of all vehicles on the other axis in a graph with horizontal columns.

    :param title: Name of the graph
    :type title: str
    :param data: Data to display in graph
    :type data: list[dict[str,int]]
    :param max: Maximum value on x axis
    :type max: int
    :param numOfEntries: Number of stops, used to calculate height of the graph
    :type numOfEntries: int
    :param leftMargin: Left margin is needed so even the long names of the bus stops are visible
    :type leftMargin: int
    :return: Bus stop chart component
    :rtype: rx.Component
    """
    return rx.card(
        rx.vstack(
            rx.heading(title, size="4"),
            rx.recharts.bar_chart(
                rx.recharts.bar(
                    data_key="load",
                    fill=rx.color("accent", 8),
                ),
                rx.recharts.x_axis(type_="number", domain=[0, max]),
                rx.recharts.y_axis(data_key="name", type_="category"),
                data=data,
                width="100%",
                height=50*numOfEntries,
                layout="vertical",
                margin={
                    "top": 0,
                    "right": 0,
                    "left": leftMargin*7,
                    "bottom": 0,
                },
            ),
            rx.text("Naplnenosť vozidla"),
            align_items="center",
        ),
        size="3",
        width="100%",
    ),