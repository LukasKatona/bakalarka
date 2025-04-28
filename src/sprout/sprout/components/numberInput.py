import reflex as rx

def numberImput(title: str, placeholder: str, value: int | float, onChangeMethod, min: str| None, max: str | None, constraint: bool, disabled = False) -> rx.Component:
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