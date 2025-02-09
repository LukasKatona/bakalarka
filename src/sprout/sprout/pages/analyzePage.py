import reflex as rx
import os

from ..backend.InputParser import InputParser
from ..backend.Simulation import Simulation
from ..backend.Statistics import Statistics

from ..components.layout import layout
from ..components.fileUpload import fileUpload
from ..components.infoCard import infoCard
from ..components.hourChart import hourChart

def getTextFromTXT(fileName: str) -> rx.Component:
    file_path = os.path.join(os.path.dirname(__file__), fileName)
    with open(file_path, "r") as file:
        content = file.read()
    return rx.text(content, white_space="pre")

def getFilePath(fileName: str) -> str:
    return os.path.join(os.path.dirname(__file__), fileName)

class AnalyzePageState(rx.State):
    bus_stops_filecontent: str = ""
    time_table_filecontent: str = ""

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
        self.bus_stops_filecontent = uploadBusStops[0].file.read().decode('utf-8')

    @rx.event
    async def handle_upload_time_table(self, uploadTimeTable: list[rx.UploadFile]):
        self.time_table_filecontent = uploadTimeTable[0].file.read().decode('utf-8')

    @rx.event
    async def handle_analyze(self):
        busStops = InputParser.parseBusStopsFromString(self.bus_stops_filecontent)
        timeTable = InputParser.parseTimeTableFromString(self.time_table_filecontent)
        stats = Simulation.run(0, 24*60, busStops, timeTable)

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
            self.loadPerBusStop.append({"name": stat[0], "load": int(round(stat[1]))})
        self.loadInPercentPerBusStop = []
        for stat in stats.busStatistics.loadInPercentPerBusStop:
            self.loadInPercentPerBusStop.append({"name": stat[0], "load": int(round(stat[1]*100))})

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
        rx.hstack(
            rx.button(
                rx.heading("Analyzovať"),
                on_click=[
                    AnalyzePageState.handle_upload_bus_stops(rx.upload_files("upload_bus_stops")),
                    AnalyzePageState.handle_upload_time_table(rx.upload_files("upload_time_table")),
                    AnalyzePageState.handle_analyze(),
                ],
                size="4",
            ),
            width="100%",
            justify="center",
        ),
        rx.cond(
            AnalyzePageState.showAnalysis,
            rx.vstack(
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
                    infoCard("Celkový počet cestujúcich čakajúcich na ďalší spoj", AnalyzePageState.totalPassengersWaitingForNextBus),
                    infoCard("Celkový počet cestujúcich, ktorí nenastúpili", AnalyzePageState.totalPassangersLeftUnboarded),
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
                rx.card(
                    rx.vstack(
                        rx.heading("Priemerná naplnenosť naprieč zastávkami", size="4"),
                        rx.recharts.bar_chart(
                            rx.recharts.bar(
                                data_key="load",
                                fill=rx.color("accent", 8),
                            ),
                            rx.recharts.x_axis(type_="number", domain=[0, AnalyzePageState.capacity]),
                            rx.recharts.y_axis(data_key="name", type_="category"),
                            data=AnalyzePageState.loadPerBusStop,
                            width="100%",
                            height=250,
                            layout="vertical",
                            margin={
                                "top": 20,
                                "right": 20,
                                "left": 100,
                                "bottom": 20,
                            },
                        ),
                        rx.text("Hodina"),
                        align_items="center",
                    ),
                    size="3",
                    width="100%",
                ),
                rx.card(
                    rx.vstack(
                        rx.heading("Priemerná naplnenosť naprieč zastávkami v percent8ch", size="4"),
                        rx.recharts.bar_chart(
                            rx.recharts.bar(
                                data_key="load",
                                fill=rx.color("accent", 8),
                            ),
                            rx.recharts.x_axis(type_="number", domain=[0, 100]),
                            rx.recharts.y_axis(data_key="name", type_="category"),
                            data=AnalyzePageState.loadInPercentPerBusStop,
                            width="100%",
                            height=250,
                            layout="vertical",
                            margin={
                                "top": 20,
                                "right": 20,
                                "left": 100,
                                "bottom": 20,
                            },
                        ),
                        rx.text("Hodina"),
                        align_items="center",
                    ),
                    size="3",
                    width="100%",
                ),
                spacing="5",
                width="100%",
            ),
        ),
        spacing="5",
        width="100%",
    )