import reflex as rx

def busStopTableTimeRow(row):
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

def busStopTableIconRow(row):
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

def busStopTableNameRow(row):
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

def busStopTableRows(rows, content, flex):
    return rx.vstack(
        rx.foreach(
            rows,
            content,
        ),
        width="100%",
        spacing="0",
        flex=flex,
    )

def busStopTable(busStops) -> rx.Component:
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