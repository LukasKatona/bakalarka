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
                        width="2.25em",
                        height="auto",
                    ),
                    dark=rx.image(
                        src="/logo-white.svg",
                        width="2.25em",
                        height="auto",
                    ),
                ),
                rx.heading(
                    "Sprout", size="7", weight="bold",
                ),
                align_items="center",
                on_click=rx.redirect("/"),
            ),
            rx.hstack(
                navbar_item("chart-column", "Analýza", "/analyze"),
                navbar_item("cog", "Optimalizácia", "/optimize"),
                rx.color_mode.button(),
                justify="end",
                align_items="center",
                spacing="5",
            ),
            justify="between",
            align_items="center",
        ),
        bg=rx.color("accent", 5),
        padding="1em",
        # position="fixed",
        # top="0px",
        # z_index="5",
        width="100%",
    )