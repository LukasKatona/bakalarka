import reflex as rx
import os

from ..components.layout import layout
from ..components.fileUpload import fileUpload
from ..components.analyze import analyze as analyzeComponent

def getTextFromTXT(fileName: str) -> rx.Component:
    file_path = os.path.join(os.path.dirname(__file__), fileName)
    with open(file_path, "r") as file:
        content = file.read()
    return rx.text(content, white_space="pre")

def getFilePath(fileName: str) -> str:
    return os.path.join(os.path.dirname(__file__), fileName)

class AnalyzePageState(rx.State):
    bus_stops_filecontent: str
    time_table_filecontent: str

    @rx.event
    async def handle_upload_bus_stops(self, uploadBusStops: list[rx.UploadFile]):
        self.bus_stops_filecontent = uploadBusStops[0].file.read().decode('utf-8')

    @rx.event
    async def handle_upload_time_table(self, uploadTimeTable: list[rx.UploadFile]):
        self.time_table_filecontent = uploadTimeTable[0].file.read().decode('utf-8')

def analyze() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.hstack(
                    rx.heading("Informácie o zastávkach"),
                    rx.dialog.root(
                        rx.dialog.trigger(rx.icon("info")),
                        rx.dialog.content(
                            rx.dialog.title("zastavky.txt"),
                            rx.dialog.description(
                                getTextFromTXT("zastavky.txt"),
                            ),
                            rx.flex(
                                rx.dialog.close(
                                    rx.button(
                                        "Zatvoriť",
                                        variant="soft",
                                        color_scheme="gray",
                                    ),
                                ),
                                rx.dialog.close(
                                    rx.button(
                                        "Stiahnuť",
                                        on_click=rx.download(url="/zastavky.txt"),
                                    ),
                                ),
                                spacing="3",
                                justify="end",
                            ),
                            max_width="fit-content",
                        ),
                    ),
                    align_items="center",
                ),
                fileUpload(
                "upload_bus_stops",
                "Nahrajte .txt súbor s infomáciami o zastávkach.",
                "Nahrať súbor",
                ),
                
                flex="1",
            ),
            rx.vstack(
                rx.hstack(
                    rx.heading("Informácie o časovom rozpise linky"),
                    rx.dialog.root(
                        rx.dialog.trigger(rx.icon("info")),
                        rx.dialog.content(
                            rx.dialog.title("rozpis.txt"),
                            rx.dialog.description(
                                getTextFromTXT("rozpis.txt"),
                            ),
                            rx.flex(
                                rx.dialog.close(
                                    rx.button(
                                        "Zatvoriť",
                                        variant="soft",
                                        color_scheme="gray",
                                    ),
                                ),
                                rx.dialog.close(
                                    rx.button(
                                        "Stiahnuť",
                                        on_click=rx.download(url="/rozpis.txt"),
                                    ),
                                ),
                                spacing="3",
                                justify="end",
                            ),
                            max_width="fit-content",
                        ),
                    ),
                    align_items="center",
                ),
                fileUpload(
                    "upload_time_table",
                    "Nahrajte .txt súbor s infomáciami o časovom rozpise linky.",
                    "Nahrať súbor",
                ),
                
                flex="1",
            ),
            width="100%",
        ),
        rx.button(
            "Analyzovať",
            on_click=[
                AnalyzePageState.handle_upload_bus_stops(rx.upload_files("upload_bus_stops")),
                AnalyzePageState.handle_upload_time_table(rx.upload_files("upload_time_table")),
            ]
        ),
        rx.cond(
            AnalyzePageState.bus_stops_filecontent,
            rx.text(AnalyzePageState.bus_stops_filecontent, white_space="pre"),
        ),
        rx.cond(
            AnalyzePageState.time_table_filecontent,
            rx.text(AnalyzePageState.time_table_filecontent, white_space="pre"),
        ),
        spacing="5",
        width="100%",
    )