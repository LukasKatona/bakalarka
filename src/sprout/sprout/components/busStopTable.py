"""
This file contains components for a table displaying list of bus stops.
"""

import reflex as rx

def busStopTableTimeRow(row: tuple[str, str, bool]) -> rx.Component:
    """
    Time part of one row in a table.

    :param row: Row data to display
    :type row: tuple[str, str, bool]
    :return: Row component
    :rtype: rx.Component
    """
    timeDelta, name, even = row[0], row[1], row[2]
    return rx.cond(
        even,
        rx.box(
            rx.hstack(
                rx.cond(
                    timeDelta == 0,
                    rx.icon("arrow-down"),
                    rx.text(timeDelta, align="right", width="100%"),
                ),
                width="100%",
            ),
            padding_x="0.5em",
            padding_y="0.125em",
            width="100%",
        ),
        rx.box(
            rx.hstack(
                rx.cond(
                    timeDelta == 0,
                    rx.icon("arrow-down", size=28),
                    rx.text(timeDelta, align="right", width="100%"),
                ),
                width="100%",
            ),
            padding_x="0.5em",
            padding_y="0.125em",
            width="100%",
            bg=rx.color("gray", 3),
        )
    )

def busStopTableIconRow(row: tuple[str, str, bool]) -> rx.Component:
    """
    Icon part of one row in a table.

    :param row: Row data to display
    :type row: tuple[str, str, bool]
    :return: Row component
    :rtype: rx.Component
    """
    timeDelta, name, even = row[0], row[1], row[2]
    return rx.cond(
        even,
        rx.box(
            rx.hstack(
                rx.icon("git-commit-vertical", size=28),
            ),
            width="100%",
            height="100%",
        ),
        rx.box(
            rx.hstack(
                rx.icon("git-commit-vertical", size=28),
            ),
            width="100%",
            height="100%",
            bg=rx.color("gray", 3),
        )
    )

def busStopTableNameRow(row: tuple[str, str, bool]) -> rx.Component:
    """
    Bus stop name part of one row in a table.

    :param row: Row data to display
    :type row: tuple[str, str, bool]
    :return: Row component
    :rtype: rx.Component
    """
    timeDelta, name, even = row[0], row[1], row[2]
    return rx.cond(
        even,
        rx.box(
            rx.hstack(
                rx.text(name),
            ),
            padding_x="0.5em",
            padding_y="0.125em",
            width="100%",
        ),
        rx.box(
            rx.hstack(
                rx.text(name),
            ),
            padding_x="0.5em",
            padding_y="0.125em",
            width="100%",
            bg=rx.color("gray", 3),
        )
    )

def busStopTableRows(rows: list[tuple[str, str, bool]], content, flex: str) -> rx.Component:
    """
    Wraps all rows in a vertical stack.

    :param rows: Rows data to display
    :type rows: list[tuple[str, str, bool]]
    :param content: Type of content, time, icon or name
    :type content: function
    :param flex: Flex of the column
    :type flex: str
    :return: Column with all the rows
    :rtype: rx.Component
    """
    return rx.vstack(
        rx.foreach(
            rows,
            content,
        ),
        width="100%",
        spacing="0",
        flex=flex,
    )

def busStopTable(busStops: list[tuple[str, str, bool]]) -> rx.Component:
    """
    Table with all the bus stops on the line with coresponding time it takes to get there.

    :param busStops: Data to display
    :type busStops: list[tuple[str, str, bool]]
    :return: Bus stop table component
    :rtype: rx.Component
    """
    return rx.card(
        rx.vstack(
            rx.heading("Zastávky linky", size="4", padding_x="3em"),
            rx.hstack(
                busStopTableRows(busStops, busStopTableTimeRow, "0"),
                busStopTableRows(busStops, busStopTableIconRow, "0"),
                busStopTableRows(busStops, busStopTableNameRow, "1"),
                spacing="0",
                width="100%",
                align="stretch",
            ),
        ),
        size="3",
        padding_x="0rem",
    ),