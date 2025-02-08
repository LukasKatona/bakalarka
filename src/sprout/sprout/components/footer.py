import reflex as rx

def footer() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.text("© 2025 Sprout", size="3", weight="medium", flex="1"),
            rx.logo(flex="1"),
            rx.text("Made by xkaton00", size="3", weight="medium", flex="1", align="right"),
            align_items="center",
        ),
        bg=rx.color("accent", 2),
        padding_x="1em",
        width="100%",
    )