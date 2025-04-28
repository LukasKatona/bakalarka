"""
This file contains simple number input component.
"""

import reflex as rx

def numberImput(title: str, placeholder: str, value: int | float, onChangeMethod, min: str| None, max: str | None, constraint: bool, disabled = False) -> rx.Component:
    """
    Number input component.

    :param title: Name of the value
    :type title: str
    :param placeholder: Placeholder text
    :type placeholder: str
    :param value: Value to change and display
    :type value: int | float
    :param onChangeMethod: Method that is triggered on input change
    :type onChangeMethod: function
    :param min: Minimal value
    :type min: str | None
    :param max: Maximal value
    :type max: str | None
    :param constraint: Constraints to validate
    :type constraint: bool
    :param disabled: Disabled if True, defaults to False
    :type disabled: bool, optional
    :return: Number input component
    :rtype: rx.Component
    """
    return rx.vstack(
        rx.text(title),
        rx.input(
            placeholder=placeholder,
            value=value,
            on_change=onChangeMethod,
            width="100%",
            size="3",
            min=min,
            max=max,
            type="number",
            color_scheme=rx.cond(
                constraint,
                "red",
                "dark"
            ),
            variant=rx.cond(
                constraint,
                "soft",
                "classic"
            ),
            disabled=rx.cond(
                disabled,
                True,
                False,
            ),
        ),
        width="100%",
        justify="between",
    ),