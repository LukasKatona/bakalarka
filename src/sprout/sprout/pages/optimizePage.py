"""
This file contians optimize page component.
"""

import reflex as rx

from ..components.infoUpload import infoUpload
from ..components.optimizeLine import optimizeLine
from ..components.optimizeLine import OptimizeLineState

def optimizePage() -> rx.Component:
    """
    Optimize page component with information uploaders and component for line optimization.

    :return: Optimize page component
    :rtype: rx.Component
    """
    return rx.vstack(
        infoUpload(OptimizeLineState),
        optimizeLine(),
        spacing="5",
        width="100%",
    )