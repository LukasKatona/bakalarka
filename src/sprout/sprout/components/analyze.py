import reflex as rx

def analyze() -> rx.Component:
    return rx.box(
        rx.text("Welcome to Analysis!!!"),
        width="100%",
    )