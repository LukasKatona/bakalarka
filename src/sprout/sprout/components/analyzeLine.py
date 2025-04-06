import reflex as rx

from ..backend.InputParser import InputParser
from ..backend.Simulation import Simulation
from ..backend.Statistics import Statistics

from .infoCard import infoCard
from .hourChart import hourChart
from .busStopChart import busStopChart

class AnalyzeLineState(rx.State):
    selectedTimeTableName: str
    selectedTimeTable: str

    busSopsFilename: str = ""
    selectedBusStops: str = ""
    timeTableFilename: str = ""
    busStopTable: list[tuple[str, str, bool]] = []
    timeTable: list[tuple[str, str, bool]] = []
    
    numberOfBusStops: int
    longestBusStopNameLength: int

    totalNumberOfBuses: int
    totalPassengersArrived: int
    totalPassengersDeparted: int
    totalPassengersLeftUnboarded: str
    totalTimeSpentWaiting: str
    averageTimeSpentWaiting: str
    passengersArrivedPerHour = []
    passengersDepartedPerHour = []
    passengersLeftUnboardedPerHour = []
    timeSpentWaitingPerHour = []

    vehicleCapacity: int = 80
    vehicleSeats: int = 30

    averageLoad: str
    averageLoadInPercent: str
    totalPassengersTransported: int
    averagePassengerSatisfaction: str
    loadPerBusStop = []
    loadInPercentPerBusStop = []

    showAnalysis: bool = False

    @rx.event
    async def clear_files(self):
        self.busSopsFilename = ""
        self.selectedBusStops = ""
        self.timeTableFilename = ""
        self.selectedTimeTable = ""
        self.selectedTimeTableName = ""
        self.busStopTable = []
        self.timeTable = []
        self.showAnalysis = False
        self.vehicleCapacity = 80
        self.vehicleSeats = 30

    @rx.event
    async def handle_analyze(self):
        if not self.selectedBusStops or not self.selectedTimeTable:
            return

        busStops = InputParser.parseBusStopsFromString(self.selectedBusStops)
        timeTable = InputParser.parseTimeTableFromString(self.selectedTimeTable)
        stats = Simulation.runMultipleThanAverage(0, 24*60, busStops, timeTable, self.vehicleCapacity, self.vehicleSeats, 50)

        self.numberOfBusStops = len(busStops)
        self.longestBusStopNameLength = max([len(busStop.name) for busStop in busStops])

        self.totalNumberOfBuses = stats.totalNumberOfBuses

        self.totalPassengersArrived = stats.busStopStatistics.totalPassengersArrived
        self.totalPassengersDeparted = stats.busStopStatistics.totalPassengersDeparted
        self.totalPassengersLeftUnboarded = str(stats.busStopStatistics.totalPassengersLeftUnboarded) + " (" + str(round(stats.busStopStatistics.totalPassengersLeftUnboarded / stats.busStopStatistics.totalPassengersArrived * 100, 2)) + "%)"
        self.totalTimeSpentWaiting = str(int(round(stats.busStopStatistics.totalTimeSpentWaiting)))
        self.averageTimeSpentWaiting = str(int(round(stats.busStopStatistics.totalTimeSpentWaiting / stats.busStopStatistics.totalPassengersArrived)))

        self.passengersArrivedPerHour = [{"hour": hour, "count": 0} for hour in range(24)]
        for stat in stats.busStopStatistics.passengersArrivedPerHour:
            self.passengersArrivedPerHour[int(stat[0])]["count"] = stat[1]
        self.passengersDepartedPerHour = [{"hour": hour, "count": 0} for hour in range(24)]
        for stat in stats.busStopStatistics.passengersDepartedPerHour:
            self.passengersDepartedPerHour[int(stat[0])]["count"] = stat[1]
        self.passengersLeftUnboardedPerHour = [{"hour": hour, "count": 0} for hour in range(24)]
        for stat in stats.busStopStatistics.passengersLeftUnboardedPerHour:
            self.passengersLeftUnboardedPerHour[int(stat[0])]["count"] = stat[1]
        self.timeSpentWaitingPerHour = [{"hour": hour, "count": 0} for hour in range(24)]
        for stat in stats.busStopStatistics.timeSpentWaitingPerHour:
            self.timeSpentWaitingPerHour[int(stat[0])]["count"] = stat[1]

        self.averageLoad = str(int(round(stats.busStatistics.averageLoad)))
        self.averageLoadInPercent = str(int(round(stats.busStatistics.averageLoadInPercent*100)))
        self.totalPassengersTransported = stats.busStatistics.totalPassengersTransported
        self.averagePassengerSatisfaction = str(int(round(stats.averagePassengerSatisfaction*100)))

        self.loadPerBusStop = []
        for stat in stats.busStatistics.loadPerBusStop:
            name = stat[0].replace(" ", "\u00A0")
            self.loadPerBusStop.append({"name": name, "load": int(round(stat[1]))})
        self.loadInPercentPerBusStop = []
        for stat in stats.busStatistics.loadInPercentPerBusStop:
            name = stat[0].replace(" ", "\u00A0")
            self.loadInPercentPerBusStop.append({"name": name, "load": int(round(stat[1]*100))})

        

        self.showAnalysis = True


def analyzeLine() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.text("Kapacita vozidla"),
                rx.input(
                    placeholder="Kapacita vozidla",
                    value=AnalyzeLineState.vehicleCapacity,
                    on_change=AnalyzeLineState.set_vehicleCapacity,
                    width="100%",
                    size="3",
                    min="0",
                    type="number",
                    color_scheme=rx.cond(
                        AnalyzeLineState.vehicleCapacity < 1,
                        "red",
                        "dark"
                    ),
                    variant=rx.cond(
                        AnalyzeLineState.vehicleCapacity < 1,
                        "soft",
                        "classic"
                    ),
                ),
                width="100%",
                justify="between",
            ),
            rx.vstack(
                rx.text("Miest na sedenie"),
                rx.input(
                    placeholder="Miest na sedenie",
                    value=AnalyzeLineState.vehicleSeats,
                    on_change=AnalyzeLineState.set_vehicleSeats,
                    width="100%",
                    size="3",
                    min="0",
                    type="number",
                    color_scheme=rx.cond(
                        AnalyzeLineState.vehicleSeats < 0,
                        "red",
                        "dark"
                    ),
                    variant=rx.cond(
                        AnalyzeLineState.vehicleSeats < 0,
                        "soft",
                        "classic"
                    ),
                ),
                width="100%",
                justify="between",
            ),
            width="100%",
            spacing="5",
            align="stretch",
        ),
        rx.hstack(
            rx.button(
                rx.heading("Vymazať súbory", size="3"),
                on_click=AnalyzeLineState.clear_files(),
                size="3",
            ),
            rx.button(
                rx.heading("Analyzovať", size="3"),
                on_click=AnalyzeLineState.handle_analyze(),
                size="3",
                disabled=rx.cond(
                    (AnalyzeLineState.selectedBusStops == "") | (AnalyzeLineState.selectedTimeTable == ""),
                    True,
                    False,
                ),
            ),
            width="100%",
            justify="center",
        ),
        rx.cond(
            AnalyzeLineState.showAnalysis,
            rx.vstack(
                rx.hstack(
                    rx.heading("Výsledky analýzy", size="8"),
                    padding_y="1em",
                    width="100%",
                    justify="center",
                ),
                rx.hstack(
                    infoCard("Celkový počet príchodov cestujúcich", AnalyzeLineState.totalPassengersArrived),
                    infoCard("Celkový počet prevezených cestujúcich", AnalyzeLineState.totalPassengersTransported),
                    infoCard("Celkový počet odchodov cestujúcich", AnalyzeLineState.totalPassengersDeparted),
                    spacing="5",
                    width="100%",
                    align_items="stretch",
                ),
                rx.hstack(
                    infoCard("Celkový čas strávený čakaním", AnalyzeLineState.totalTimeSpentWaiting + " min"),
                    infoCard("Priemerný čas strávený čakaním", AnalyzeLineState.averageTimeSpentWaiting + " min"),
                    spacing="5",
                    width="100%",
                    align_items="stretch",
                ),
                rx.hstack(
                    infoCard("Počet prípadov kedy sa cestujúci nezmestil do vozidla", AnalyzeLineState.totalPassengersLeftUnboarded),
                    infoCard("Priemerná spokojnosť cestujúcich", AnalyzeLineState.averagePassengerSatisfaction + "%"),
                    spacing="5",
                    width="100%",
                    align_items="stretch",
                ),
                hourChart("Cestujúci prichádzajúci za hodinu", AnalyzeLineState.passengersArrivedPerHour),
                hourChart("Cestujúci vystupujúci za hodinu", AnalyzeLineState.passengersDepartedPerHour),
                hourChart("Čas strávený čakaním za hodinu", AnalyzeLineState.timeSpentWaitingPerHour),
                hourChart("Počet prípadov kedy sa cestujúci nezmestil do vozidla za hodinu", AnalyzeLineState.passengersLeftUnboardedPerHour),
                rx.hstack(
                    infoCard("Celkový počet vozidiel", AnalyzeLineState.totalNumberOfBuses),
                    infoCard("Priemerná naplnenosť vozidiel", AnalyzeLineState.averageLoad + " cestujúcich"),
                    infoCard("Priemerná naplnenosť vozidiel", AnalyzeLineState.averageLoadInPercent + "%"),
                    spacing="5",
                    width="100%",
                    align_items="stretch",
                ),
                busStopChart("Priemerná naplnenosť naprieč zastávkami", AnalyzeLineState.loadPerBusStop, AnalyzeLineState.vehicleCapacity, AnalyzeLineState.numberOfBusStops, AnalyzeLineState.longestBusStopNameLength),
                busStopChart("Priemerná naplnenosť naprieč zastávkami v percentách", AnalyzeLineState.loadInPercentPerBusStop, 100, AnalyzeLineState.numberOfBusStops, AnalyzeLineState.longestBusStopNameLength),
                spacing="5",
                width="100%",
            ),
        ),
        spacing="5",
        width="100%",
    ),