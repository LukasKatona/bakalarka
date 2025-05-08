"""
This file contains info upload component and its state.

:author: Lukas Katona
"""

import os
import reflex as rx

from ..backend.InputParser import InputParser

from .busStopTable import busStopTable
from .timeTable import timeTable
from .analyzeLine import AnalyzeLineState
from .optimizeLine import OptimizeLineState


def getTextFromTXT(fileName: str) -> rx.Component:
    """
    This function opens the file and extracts the text inside.

    :param fileName: Name of the given file
    :type fileName: str
    :return: Text from the file
    :rtype: rx.Component
    """
    file_path = os.path.join(os.path.dirname(__file__), fileName)
    with open(file_path, "r") as file:
        content = file.read()
    return rx.text(content, white_space="pre")

def getFilePath(fileName: str) -> str:
    """
    Helper function for modifying the file name.

    :param fileName: File name to modify
    :type fileName: str
    :return: Modified file name
    :rtype: str
    """
    return os.path.join(os.path.dirname(__file__), fileName)

class InfoUploadState(rx.State):
    options: list[tuple[str, str]] = []
    dropdownOptions: list[str] = []

    @rx.event
    async def selectTimeTableFromDropdown(self, value: str): 
        """
        Selects timetable from dropdown.

        :param value: Selected timetable name
        :type value: str
        """
        if self.router.page.path == "/analyze":
            stateClass = AnalyzeLineState
        if self.router.page.path == "/optimize":
            stateClass = OptimizeLineState
        state = await self.get_state(stateClass)
        state.selectedTimeTableName = value
        state.selectedTimeTable = next((option[1] for option in self.options if option[0] == value), None)
        state.timeTableFilename = ''
        state.timeTable = self.parseTimeTableToTuple(state.selectedTimeTable)

    def insertNewTimeTable(self, timeTable: tuple[str, str]):
        """
        Inserts new timetable to dropdown options

        :param timeTable: Timetable to insert
        :type timeTable: tuple[str, str]
        """
        self.options.append(timeTable)
        self.dropdownOptions.append(timeTable[0])

    def parseBusStopsToTuple(self, selectedBusStops: str) -> list[tuple[str, str, bool]]:
        """
        Parses the text containing information about bus stops.

        :param selectedBusStops: Bus stops information
        :type selectedBusStops: str
        :return: List of formated bus stops
        :rtype: list[tuple[str, str, bool]]
        """
        busStops = InputParser.parseBusStopsFromString(selectedBusStops)
        busStopTuple: list[tuple[str, str, bool]] = []
        even = True
        for busStop in busStops:
            busStopTuple.append((busStop.timeDeltaToArrive, busStop.name, even))
            even = not even
        return busStopTuple

    def parseTimeTableToTuple(self, selectedTimeTable: str) -> list[tuple[str, str, bool]]:
        """
        Parses the text containing niformation about timetable.

        :param selectedTimeTable: Timetable information
        :type selectedTimeTable: str
        :return: Formated timetable
        :rtype: list[tuple[str, str, bool]]
        """
        timeTable = InputParser.parseTimeTableFromString(selectedTimeTable)
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
    async def handleUploadBusStops(self, uploadBusStops: list[rx.UploadFile]):
        """
        Uploads text file containing information about bus stops.

        :param uploadBusStops: Bus stop file
        :type uploadBusStops: list[rx.UploadFile]
        """
        if self.router.page.path == "/analyze":
            stateClass = AnalyzeLineState
        if self.router.page.path == "/optimize":
            stateClass = OptimizeLineState
        state = await self.get_state(stateClass)
        state.busSopsFilename = uploadBusStops[0].filename
        state.selectedBusStops = uploadBusStops[0].file.read().decode('utf-8')
        state.busStopTable = self.parseBusStopsToTuple(state.selectedBusStops)
        if self.router.page.path == "/optimize":
            state.initConstraints()
        
    @rx.event
    async def handleUploadTimeTable(self, uploadTimeTable: list[rx.UploadFile]):
        """
        Uploads text file containing information about timetable.

        :param uploadTimeTable: Timetable file
        :type uploadTimeTable: list[rx.UploadFile]
        """
        if self.router.page.path == "/analyze":
            stateClass = AnalyzeLineState
        if self.router.page.path == "/optimize":
            stateClass = OptimizeLineState
        state = await self.get_state(stateClass)
        state.selectedTimeTableName = ''
        state.timeTableFilename = uploadTimeTable[0].filename
        state.selectedTimeTable = uploadTimeTable[0].file.read().decode('utf-8')
        state.timeTable = self.parseTimeTableToTuple(state.selectedTimeTable)
        
def infoUpload(stateClass) -> rx.Component:
    """
    Info upload component, for uploading information about bus stops and timetable. Also displays selected bus stops and timetable.

    :param stateClass: State of the page on which is the info upload component
    :type stateClass: class
    :return: Info upload component
    :rtype: rx.Component
    """
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
                            stateClass.busSopsFilename != "",
                            rx.text(stateClass.busSopsFilename),
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
                    on_drop=InfoUploadState.handleUploadBusStops(rx.upload_files("upload_bus_stops")),
                ),              
                flex="1",
            ),
            rx.cond(
                stateClass == AnalyzeLineState,
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
                                stateClass.timeTableFilename != "",
                                rx.text(stateClass.timeTableFilename),
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
                        on_drop=InfoUploadState.handleUploadTimeTable(rx.upload_files("upload_time_table")),
                    ),
                    rx.center(
                        rx.divider(),
                        rx.text("alebo"),
                        rx.divider(),
                        width="100%",
                        spacing="3",
                    ),
                    rx.select(
                        InfoUploadState.dropdownOptions,  
                        value=stateClass.selectedTimeTableName,
                        on_change=InfoUploadState.selectTimeTableFromDropdown,
                        size='3',
                        width="100%",
                    ),                 
                    flex="1",
                ),
            ),
            spacing="5",
            align_items="stretch",
            width="100%",
        ),
        rx.hstack(
            rx.vstack(
                rx.cond(
                    stateClass.busStopTable,
                    rx.box(
                        busStopTable(stateClass.busStopTable),
                    ),
                    rx.text("\u00A0"),
                    
                ),
                align_items=rx.cond(stateClass == AnalyzeLineState, "end", "center"),
                flex="1",
            ),
            rx.cond(
                stateClass == AnalyzeLineState,
                rx.vstack(
                    rx.cond(
                        stateClass.timeTable,
                        rx.box(
                            timeTable(stateClass.timeTable),
                        ),
                        rx.text("\u00A0"),
                    ),
                    flex="1",
                ),
            ),
            spacing="5",
            width="100%",
        ),
        spacing="5",
        width="100%",
    )