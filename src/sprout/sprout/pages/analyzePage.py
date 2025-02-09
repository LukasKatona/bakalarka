import reflex as rx
import os

from ..backend.InputParser import InputParser
from ..backend.Simulation import Simulation
from ..backend.Statistics import Statistics

from ..components.layout import layout
from ..components.infoCard import infoCard
from ..components.hourChart import hourChart
from ..components.busStopChart import busStopChart

def getTextFromTXT(fileName: str) -> rx.Component:
    file_path = os.path.join(os.path.dirname(__file__), fileName)
    with open(file_path, "r") as file:
        content = file.read()
    return rx.text(content, white_space="pre")

def getFilePath(fileName: str) -> str:
    return os.path.join(os.path.dirname(__file__), fileName)

class AnalyzePageState(rx.State):
    bus_sops_filename: str = ""
    bus_stops_filecontent: str = ""
    time_table_filename: str = ""
    time_table_filecontent: str = ""

    numberOfBusStops: int
    longestBusStopNameLength: int

    totalNumberOfBuses: int
    totalPassengersArrived: int
    totalPassengersDeparted: int
    totalPassengersWaitingForNextBus: int
    totalTimeSpentWaiting: str
    averageTimeSpentWaiting: str
    totalPassangersLeftUnboarded: int
    passengersArrivedPerHour = []
    passengersDepartedPerHour = []
    passengersWaitingForNextBusPerHour = []
    timeSpentWaitingPerHour = []

    capacity: int
    averageLoad: str
    averageLoadInPercent: str
    totalPassengersTransported: int
    loadPerBusStop = []
    loadInPercentPerBusStop = []

    showAnalysis: bool = False

    @rx.event
    async def handle_upload_bus_stops(self, uploadBusStops: list[rx.UploadFile]):
        self.bus_sops_filename = uploadBusStops[0].filename
        self.bus_stops_filecontent = uploadBusStops[0].file.read().decode('utf-8')

    @rx.event
    async def handle_upload_time_table(self, uploadTimeTable: list[rx.UploadFile]):
        self.time_table_filename = uploadTimeTable[0].filename
        self.time_table_filecontent = uploadTimeTable[0].file.read().decode('utf-8')

    @rx.event
    async def handle_analyze(self):
        busStops = InputParser.parseBusStopsFromString(self.bus_stops_filecontent)
        timeTable = InputParser.parseTimeTableFromString(self.time_table_filecontent)
        stats = Simulation.run(0, 24*60, busStops, timeTable)

        self.numberOfBusStops = len(busStops)
        self.longestBusStopNameLength = max([len(busStop.name) for busStop in busStops])

        self.totalNumberOfBuses = stats.totalNumberOfBuses

        self.totalPassengersArrived = stats.busStopStatistics.totalPassengersArrived
        self.totalPassengersDeparted = stats.busStopStatistics.totalPassengersDeparted
        self.totalPassengersWaitingForNextBus = stats.busStopStatistics.totalPassengersWaitingForNextBus
        self.totalTimeSpentWaiting = str(int(round(stats.busStopStatistics.totalTimeSpentWaiting)))
        self.averageTimeSpentWaiting = str(int(round(stats.busStopStatistics.totalTimeSpentWaiting / stats.busStopStatistics.totalPassengersArrived)))
        self.totalPassangersLeftUnboarded = stats.busStopStatistics.totalPassangersLeftUnboarded

        self.passengersArrivedPerHour = [{"hour": hour, "count": 0} for hour in range(24)]
        for stat in stats.busStopStatistics.passengersArrivedPerHour:
            self.passengersArrivedPerHour[int(stat[0])]["count"] = stat[1]
        self.passengersDepartedPerHour = [{"hour": hour, "count": 0} for hour in range(24)]
        for stat in stats.busStopStatistics.passengersDepartedPerHour:
            self.passengersDepartedPerHour[int(stat[0])]["count"] = stat[1]
        self.passengersWaitingForNextBusPerHour = [{"hour": hour, "count": 0} for hour in range(24)]
        for stat in stats.busStopStatistics.passengersWaitingForNextBusPerHour:
            self.passengersWaitingForNextBusPerHour[int(stat[0])]["count"] = stat[1]
        self.timeSpentWaitingPerHour = [{"hour": hour, "count": 0} for hour in range(24)]
        for stat in stats.busStopStatistics.timeSpentWaitingPerHour:
            self.timeSpentWaitingPerHour[int(stat[0])]["count"] = stat[1]

        self.capacity = stats.busStatistics.capacity
        self.averageLoad = str(int(round(stats.busStatistics.averageLoad)))
        self.averageLoadInPercent = str(int(round(stats.busStatistics.averageLoadInPercent*100)))
        self.totalPassengersTransported = stats.busStatistics.totalPassengersTransported

        self.loadPerBusStop = []
        for stat in stats.busStatistics.loadPerBusStop:
            name = stat[0].replace(" ", "\u00A0")
            self.loadPerBusStop.append({"name": name, "load": int(round(stat[1]))})
        self.loadInPercentPerBusStop = []
        for stat in stats.busStatistics.loadInPercentPerBusStop:
            name = stat[0].replace(" ", "\u00A0")
            self.loadInPercentPerBusStop.append({"name": name, "load": int(round(stat[1]*100))})

        self.showAnalysis = True

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
                rx.upload(
                    rx.vstack(
                        rx.text("Nahrajte .txt súbor s infomáciami o zastávkach."),
                        rx.button("Nahrať súbor"),
                        rx.cond(
                            AnalyzePageState.bus_sops_filename != "",
                            rx.text(AnalyzePageState.bus_sops_filename),
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
                    on_drop=AnalyzePageState.handle_upload_bus_stops(rx.upload_files("upload_bus_stops")),
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
                            AnalyzePageState.time_table_filename != "",
                            rx.text(AnalyzePageState.time_table_filename),
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
                    on_drop=AnalyzePageState.handle_upload_time_table(rx.upload_files("upload_time_table")),
                ),                   
                flex="1",
            ),
            spacing="5",
            align_items="stretch",
            width="100%",
        ),
        rx.hstack(
            rx.button(
                rx.heading("Analyzovať"),
                on_click=AnalyzePageState.handle_analyze(),
                size="4",
            ),
            width="100%",
            justify="center",
        ),
        rx.cond(
            AnalyzePageState.showAnalysis,
            rx.vstack(
                rx.hstack(
                    rx.heading("Výsledky analýzy", size="8"),
                    padding_y="1em",
                    width="100%",
                    justify="center",
                ),
                rx.hstack(
                    infoCard("Celkový počet príchodov cestujúcich", AnalyzePageState.totalPassengersArrived),
                    infoCard("Celkový počet prevezených cestujúcich", AnalyzePageState.totalPassengersTransported),
                    infoCard("Celkový počet odchodov cestujúcich", AnalyzePageState.totalPassengersDeparted),
                    spacing="5",
                    width="100%",
                    align_items="stretch",
                ),
                rx.hstack(
                    infoCard("Celkový čas strávený čakaním", AnalyzePageState.totalTimeSpentWaiting + " min"),
                    infoCard("Priemerný čas strávený čakaním", AnalyzePageState.averageTimeSpentWaiting + " min"),
                    spacing="5",
                    width="100%",
                    align_items="stretch",
                ),
                rx.hstack(
                    infoCard("Počet prípadov kedy sa cestujúci nezmestil do vozidla", AnalyzePageState.totalPassengersWaitingForNextBus),
                    infoCard("Počet cestujúcich, ktorí sa za celý deň nezmestili do jediného vozidla", AnalyzePageState.totalPassangersLeftUnboarded),
                    spacing="5",
                    width="100%",
                    align_items="stretch",
                ),
                hourChart("Cestujúci prichádzajúci za hodinu", AnalyzePageState.passengersArrivedPerHour),
                hourChart("Cestujúci vystupujúci za hodinu", AnalyzePageState.passengersDepartedPerHour),
                hourChart("Čas strávený čakaním za hodinu", AnalyzePageState.timeSpentWaitingPerHour),
                hourChart("Počet prípadov kedy sa cestujúci nezmestil do vozidla za hodinu", AnalyzePageState.passengersWaitingForNextBusPerHour),
                rx.hstack(
                    infoCard("Celkový počet vozidiel", AnalyzePageState.totalNumberOfBuses),
                    infoCard("Priemerná naplnenosť vozidiel", AnalyzePageState.averageLoad + " cestujúcich"),
                    infoCard("Priemerná naplnenosť vozidiel", AnalyzePageState.averageLoadInPercent + "%"),
                    spacing="5",
                    width="100%",
                    align_items="stretch",
                ),
                busStopChart("Priemerná naplnenosť naprieč zastávkami", AnalyzePageState.loadPerBusStop, AnalyzePageState.capacity, AnalyzePageState.numberOfBusStops, AnalyzePageState.longestBusStopNameLength),
                busStopChart("Priemerná naplnenosť naprieč zastávkami v percentách", AnalyzePageState.loadInPercentPerBusStop, 100, AnalyzePageState.numberOfBusStops, AnalyzePageState.longestBusStopNameLength),
                spacing="5",
                width="100%",
            ),
        ),
        spacing="5",
        width="100%",
    )