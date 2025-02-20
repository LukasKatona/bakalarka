import os

import reflex as rx

from ..backend.InputParser import InputParser
from .busStopTable import busStopTable
from .timeTable import timeTable

def getTextFromTXT(fileName: str) -> rx.Component:
    file_path = os.path.join(os.path.dirname(__file__), fileName)
    with open(file_path, "r") as file:
        content = file.read()
    return rx.text(content, white_space="pre")

def getFilePath(fileName: str) -> str:
    return os.path.join(os.path.dirname(__file__), fileName)

class InfoUploadState(rx.State):
    bus_sops_filename: str = ""
    bus_stops_filecontent: str = ""
    time_table_filename: str = ""
    time_table_filecontent: str = ""
    busStopTable: list[tuple[str, str, bool]]
    timeTable: list[tuple[str, str, bool]]

    def parseBusStopsToTuple(self) -> list[tuple[str, str, bool]]:
        busStops = InputParser.parseBusStopsFromString(self.bus_stops_filecontent)
        busStopTuple: list[tuple[str, str, bool]] = []
        even = True
        for busStop in busStops:
            busStopTuple.append((busStop.timeDeltaToArrive, busStop.name, even))
            even = not even
        return busStopTuple

    def parseTimeTableToTuple(self) -> list[tuple[str, str, bool]]:
        timeTable = InputParser.parseTimeTableFromString(self.time_table_filecontent)
        timeTableTuple: list[tuple[str, str, bool]] = []
        for hour in range(24):
            hourStr = str(hour).zfill(2) + ":" if hour < 10 else str(hour) + ":"
            minutes = next((row.minutes for row in timeTable.rows if row.hour == hour), None)
            minutesStr = ""
            if minutes is not None:
                for minute in minutes:
                    minutesStr += str(minute).zfill(2) + "\u00A0\u00A0"
            timeTableTuple.append((hourStr, minutesStr, hour % 2 == 0))
        return timeTableTuple

    @rx.event
    async def handle_upload_bus_stops(self, uploadBusStops: list[rx.UploadFile]):
        self.bus_sops_filename = uploadBusStops[0].filename
        self.bus_stops_filecontent = uploadBusStops[0].file.read().decode('utf-8')
        self.busStopTable = self.parseBusStopsToTuple()

    @rx.event
    async def handle_upload_time_table(self, uploadTimeTable: list[rx.UploadFile]):
        self.time_table_filename = uploadTimeTable[0].filename
        self.time_table_filecontent = uploadTimeTable[0].file.read().decode('utf-8')
        self.timeTable = self.parseTimeTableToTuple()

def infoUpload() -> rx.Component:
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
                rx.upload(
                    rx.vstack(
                        rx.text("Nahrajte .txt súbor s infomáciami o zastávkach."),
                        rx.button("Nahrať súbor"),
                        rx.cond(
                            InfoUploadState.bus_sops_filename != "",
                            rx.text(InfoUploadState.bus_sops_filename),
                            rx.text("\u00A0"),
                        ),
                        align_items="center",
                    ),
                    id="upload_bus_stops",
                    accept=".txt",
                    max_files=1,
                    padding="2em",
                    multiple=False,
                    width="100%",
                    height="100%",
                    on_drop=InfoUploadState.handle_upload_bus_stops(rx.upload_files("upload_bus_stops")),
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
                rx.upload(
                    rx.vstack(
                        rx.text("Nahrajte .txt súbor s infomáciami o časovom rozpise linky."),
                        rx.button("Nahrať súbor"),
                        rx.cond(
                            InfoUploadState.time_table_filename != "",
                            rx.text(InfoUploadState.time_table_filename),
                            rx.text("\u00A0"),
                        ),
                        align_items="center",
                    ),
                    id="upload_time_table",
                    accept=".txt",
                    max_files=1,
                    padding="2em",
                    multiple=False,
                    width="100%",
                    height="100%",
                    on_drop=InfoUploadState.handle_upload_time_table(rx.upload_files("upload_time_table")),
                ),                   
                flex="1",
            ),
            spacing="5",
            align_items="stretch",
            width="100%",
        ),

        rx.hstack(
            rx.vstack(
                rx.cond(
                    InfoUploadState.busStopTable,
                    rx.box(
                        busStopTable(InfoUploadState.busStopTable),
                    ),
                    rx.text("\u00A0"),
                    
                ),
                align_items="end",
                flex="1",
            ),
            rx.vstack(
                rx.cond(
                    InfoUploadState.timeTable,
                    rx.box(
                        timeTable(InfoUploadState.timeTable),
                    ),
                    rx.text("\u00A0"),
                ),
                flex="1",
            ),
            spacing="5",
            width="100%",
        ),

        spacing="5",
        width="100%",
    )