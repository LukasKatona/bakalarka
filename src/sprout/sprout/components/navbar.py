import reflex as rx

def navbar_item(icon: str, text: str, url: str) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon),
            rx.text(text, size="4", weight="medium"),
        ),
        href=url,
        style={"text-decoration": "none"},
    )

def navbar() -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.color_mode_cond(
                    light=rx.image(
                        src="/logo-black.svg",
                        width="2.5em",
                        height="auto",
                    ),
                    dark=rx.image(
                        src="/logo-white.svg",
                        width="2.5em",
                        height="auto",
                    ),
                ),
                rx.vstack(
                    rx.heading(
                        "SPROUT", size="5", weight="bold",
                    ),
                    rx.text("Smart Performance & Resource Optimization for Urban Transport", size="2"),
                    justify="center",
                    spacing="0",
                ),
                align_items="center",
                on_click=rx.redirect("/"),
            ),
            rx.hstack(
                navbar_item("chart-column", "Analýza linky", "/analyze"),
                navbar_item("cog", "Optimalizácia linky", "/optimize"),
                rx.color_mode.button(),
                justify="end",
                align_items="center",
                spacing="5",
            ),
            justify="between",
            align_items="center",
            height="100%",
        ),
        bg=rx.color("accent", 5),
        padding="1em",
        position="fixed",
        top="0px",
        z_index="5",
        width="100%",
        height="5em",
    )