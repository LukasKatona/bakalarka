import reflex as rx


def infoCard(title: str, info: str) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(title, size="4"),
            rx.heading(info, size="8"),
            align_items="center",
            justify="between",
            height="100%",
        ),
        size="3",
        width="100%",
    ),
