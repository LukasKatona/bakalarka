"""
This file contains components for vehicle timetable with its departures.

:author: Lukas Katona
"""

import reflex as rx

def timeTableRow(row: tuple[str, str, bool]) -> rx.Component:
    """
    One row of the timetablle

    :param row: Row data to display
    :type row: tuple[str, str, bool]
    :return: Row component
    :rtype: rx.Component
    """
    hour, minutes, even = row[0], row[1], row[2]
    return rx.cond(
        even,
        rx.box(
            rx.hstack(
                rx.text(hour),
                rx.text(minutes),
            ),
            padding_x="0.5em",
            padding_y="0.125em",
            width="100%",
        ),
        rx.box(
            rx.hstack(
                rx.text(hour),
                rx.text(minutes),
            ),
            padding_x="0.5em",
            padding_y="0.125em",
            width="100%",
            bg=rx.color("gray", 3),
        )
    )

def timeTableRows(rows: list[tuple[str, str, bool]]) -> rx.Component:
    """
    Wraps all rows in vertical stack.

    :param rows: Rows data to display
    :type rows: list[tuple[str, str, bool]]
    :return: Column with all the rows
    :rtype: rx.Component
    """
    return rx.vstack(
        rx.foreach(
            rows,
            timeTableRow,
        ),
        width="100%",
        spacing="0",
    )

def timeTable(timeTable: list[tuple[str, str, bool]], heading: str = "Časový rozpis linky") -> rx.Component:
    """
    Timetable with departures of the vehicle.

    :param timeTable: Data to display
    :type timeTable: list[tuple[str, str, bool]]
    :param heading: Name of the timetable, defaults to "Časový rozpis linky"
    :type heading: str, optional
    :return: Timetable component
    :rtype: rx.Component
    """
    return rx.card(
        rx.vstack(
            rx.heading(heading, size="4", padding_x="3em"),
            timeTableRows(timeTable),
        ),
        size="3",
        padding_x="0rem",
    ),