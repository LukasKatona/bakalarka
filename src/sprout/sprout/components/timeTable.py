import reflex as rx

def timeTableRow(row):
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

def timeTableRows(rows):
    return rx.vstack(
        rx.foreach(
            rows,
            timeTableRow,
        ),
        width="100%",
        spacing="0",
    )

def timeTable(timeTable) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading("Časový rozvrh linky", size="4", padding_x="3em"),
            timeTableRows(timeTable),
        ),
        size="3",
        padding_x="0rem",
    ),