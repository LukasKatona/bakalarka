"""
This file contains contraint hour input components.

:author: Lukas Katona
"""

import reflex as rx

def constraintHourInput(hour: int) -> rx.Component:
    """
    Number input for one hour of the day.

    :param hour: Hour of the day
    :type hour: int
    :return: Number input
    :rtype: rx.Component
    """
    from .optimizeLine import OptimizeLineState
    return rx.vstack(
        rx.input(
            type="number",
            value=OptimizeLineState.constraints[hour],
            on_change=lambda val: OptimizeLineState.changeConstraints(val, hour),
            size="3",
            radius="none",
            disabled=OptimizeLineState.optimizationRunning,
            min="0",
            color_scheme=rx.cond(
                OptimizeLineState.constraints[hour] < 0,
                "red",
                "dark"
            ),
            variant=rx.cond(
                OptimizeLineState.constraints[hour] < 0,
                "soft",
                "classic"
            ),
        ),
        rx.text(hour),
        align="center",
    )

def constraintInput() -> rx.Component:
    """
    All 24 number inputs for the whole day, used to constrain number of departures from the bus stop

    :return: 24 number inputs in a row
    :rtype: rx.Component
    """
    return rx.vstack(
        rx.text("Pevný počet spojov pre danú hodinu"),
        rx.hstack(
            constraintHourInput(0),
            constraintHourInput(1),
            constraintHourInput(2),
            constraintHourInput(3),
            constraintHourInput(4),
            constraintHourInput(5),
            constraintHourInput(6),
            constraintHourInput(7),
            constraintHourInput(8),
            constraintHourInput(9),
            constraintHourInput(10),
            constraintHourInput(11),
            constraintHourInput(12),
            constraintHourInput(13),
            constraintHourInput(14),
            constraintHourInput(15),
            constraintHourInput(16),
            constraintHourInput(17),
            constraintHourInput(18),
            constraintHourInput(19),
            constraintHourInput(20),
            constraintHourInput(21),
            constraintHourInput(22),
            constraintHourInput(23),
            spacing="0",
        ),
        width="100%",
    ),