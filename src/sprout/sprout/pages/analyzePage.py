import reflex as rx

from ..components.infoUpload import infoUpload
from ..components.analyzeLine import analyzeLine

def analyzePage() -> rx.Component:
    return rx.vstack(
        infoUpload(),
        analyzeLine(),
        spacing="5",
        width="100%",
    )