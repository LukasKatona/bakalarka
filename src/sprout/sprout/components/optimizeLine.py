import reflex as rx

class OptimizeLineState(rx.State):
    bus_sops_filename: str = ""
    bus_stops_filecontent: str = ""
    time_table_filename: str = ""
    time_table_filecontent: str = ""
    busStopTable: list[tuple[str, str, bool]] = []
    timeTable: list[tuple[str, str, bool]] = []

    @rx.event
    async def clear_files(self):
        self.bus_sops_filename = ""
        self.bus_stops_filecontent = ""
        self.time_table_filename = ""
        self.time_table_filecontent = ""
        self.busStopTable = []
        self.timeTable = []

    @rx.event
    async def handle_optimize(self):
        print("Optimizing...")

def optimizeLine() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.button(
                rx.heading("Vymazať súbory"),
                on_click=OptimizeLineState.clear_files(),
                size="4",
            ),
            rx.button(
                rx.heading("Optimalizovať"),
                on_click=OptimizeLineState.handle_optimize(),
                size="4",
                disabled=rx.cond(
                    (OptimizeLineState.bus_stops_filecontent == "") | (OptimizeLineState.time_table_filecontent == ""),
                    True,
                    False,
                ),
            ),
            width="100%",
            justify="center",
        ),
        spacing="5",
        width="100%",
    ),