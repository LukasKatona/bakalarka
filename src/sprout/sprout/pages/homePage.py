"""
This file contians home page component.
"""

import reflex as rx

def homePage() -> rx.Component:
    """
    Simple and minimalistic home page component with a welcome message.

    :return: Home page component
    :rtype: rx.Component
    """
    return rx.vstack(
        rx.vstack(
            rx.color_mode_cond(
                light=rx.image(
                    src="/logo-black.svg",
                    width="10em",
                    height="auto",
                ),
                dark=rx.image(
                    src="/logo-white.svg",
                    width="10em",
                    height="auto",
                ),
            ),
            rx.heading(
                "SPROUT", size="9", weight="bold",
            ),
            rx.text(
                "Smart Performance & Resource Optimization for Urban Transport",
                size="5"
            ),
            align_items="center",
            spacing="1",
            width="100%",
        ),
        rx.vstack(
            rx.text(
                "Táto platforma poskytuje nástroje na analýzu a optimalizáciu cestovných poriadkov mestskej dopravy. "
                "Umožňuje používateľom hodnotiť aktuálne cestovné poriadky, identifikovať neefektívnosti "
                "a implementovať riešenia založené na dátach na zlepšenie prevádzkovej výkonnosti. "
                "Cieľom je podporiť informované rozhodovanie a zefektívniť plánovanie dopravy v mestských oblastiach.",
                align="center",
            ),
            rx.hstack(
                rx.card(
                    rx.text("Analýza linky", size="5", weight="bold"),
                    rx.text(
                        "Nahrajte a preskúmajte cestovné poriadky mestskej dopravy, aby ste získali prehľad o výkonnostných ukazovateľoch. "
                        "Identifikujte slabé miesta a oblasti na zlepšenie pomocou tohto analytického nástroja."
                    ),
                    size="3",
                    width="100%",
                ),
                rx.card(
                    rx.text("Optimalizácia linky", size="5", weight="bold"),
                    rx.text(
                        "Preskúmajte optimalizované cestovné poriadky na zlepšenie efektívnosti. "
                        "Využite pokročilé algoritmy na navrhovanie efektívnych plánov dopravy, "
                        "ktoré zlepšujú prevádzkovú výkonnosť aj spokojnosť cestujúcich."
                    ),
                    size="3",
                    width="100%",
                ),
                justify="between",
                width="100%",
            ),
            align_items="center",
            spacing="5",
            width="75%",
        ),
        align_items="center",
        padding_top="3em",
        spacing="5",
    )
