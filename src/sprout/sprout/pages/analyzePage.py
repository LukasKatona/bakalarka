"""
This file contains analyze page component.

:author: Lukas Katona
"""

import reflex as rx

from ..components.infoUpload import infoUpload
from ..components.analyzeLine import analyzeLine
from ..components.analyzeLine import AnalyzeLineState

def analyzePage() -> rx.Component:
    """
    Analyze page component with information uploaders and component for line analysis.

    :return: Analyze page component
    :rtype: rx.Component
    """
    return rx.vstack(
        infoUpload(AnalyzeLineState),
        analyzeLine(),
        spacing="5",
        width="100%",
    )