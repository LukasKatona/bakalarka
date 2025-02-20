import reflex as rx

from ..components.infoUpload import infoUpload
from ..components.optimizeLine import optimizeLine

def optimizePage() -> rx.Component:
    return rx.vstack(
        infoUpload(),
        optimizeLine(),
        spacing="5",
        width="100%",
    )