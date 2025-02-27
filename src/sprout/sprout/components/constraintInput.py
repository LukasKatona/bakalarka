import reflex as rx

def constraintHourInput(hour: int) -> rx.Component:
    from .optimizeLine import OptimizeLineState
    return rx.vstack(
        rx.input(
            type="number",
            value=OptimizeLineState.constraints[hour],
            on_change=lambda val: OptimizeLineState.changeConstraints(val, hour),
            size="3",
            radius="none"
        ),
        rx.text(hour),
        align="center",
    )

def constraintInput() -> rx.Component:
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