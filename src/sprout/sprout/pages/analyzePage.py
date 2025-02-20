import reflex as rx

from ..components.infoUpload import infoUpload
from ..components.analyzeLine import analyzeLine
from ..components.analyzeLine import AnalyzeLineState

def analyzePage() -> rx.Component:
    return rx.vstack(
        infoUpload(AnalyzeLineState),
        analyzeLine(),
        spacing="5",
        width="100%",
    )