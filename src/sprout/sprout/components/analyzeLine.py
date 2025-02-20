import reflex as rx

from ..backend.InputParser import InputParser
from ..backend.Simulation import Simulation
from ..backend.Statistics import Statistics

from .infoCard import infoCard
from .hourChart import hourChart
from .busStopChart import busStopChart

class AnalyzeLineState(rx.State):
    bus_sops_filename: str = ""
    bus_stops_filecontent: str = ""
    time_table_filename: str = ""
    time_table_filecontent: str = ""
    busStopTable: list[tuple[str, str, bool]] = []
    timeTable: list[tuple[str, str, bool]] = []
    
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
    async def clear_files(self):
        self.bus_sops_filename = ""
        self.bus_stops_filecontent = ""
        self.time_table_filename = ""
        self.time_table_filecontent = ""
        self.busStopTable = []
        self.timeTable = []
        self.showAnalysis = False

    @rx.event
    async def handle_analyze(self):
        if not self.bus_stops_filecontent or not self.time_table_filecontent:
            return

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


def analyzeLine() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.button(
                rx.heading("Vymazať súbory"),
                on_click=AnalyzeLineState.clear_files(),
                size="4",
            ),
            rx.button(
                rx.heading("Analyzovať"),
                on_click=AnalyzeLineState.handle_analyze(),
                size="4",
                disabled=rx.cond(
                    (AnalyzeLineState.bus_stops_filecontent == "") | (AnalyzeLineState.time_table_filecontent == ""),
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
                    infoCard("Počet prípadov kedy sa cestujúci nezmestil do vozidla", AnalyzeLineState.totalPassengersWaitingForNextBus),
                    infoCard("Počet cestujúcich, ktorí sa za celý deň nezmestili do jediného vozidla", AnalyzeLineState.totalPassangersLeftUnboarded),
                    spacing="5",
                    width="100%",
                    align_items="stretch",
                ),
                hourChart("Cestujúci prichádzajúci za hodinu", AnalyzeLineState.passengersArrivedPerHour),
                hourChart("Cestujúci vystupujúci za hodinu", AnalyzeLineState.passengersDepartedPerHour),
                hourChart("Čas strávený čakaním za hodinu", AnalyzeLineState.timeSpentWaitingPerHour),
                hourChart("Počet prípadov kedy sa cestujúci nezmestil do vozidla za hodinu", AnalyzeLineState.passengersWaitingForNextBusPerHour),
                rx.hstack(
                    infoCard("Celkový počet vozidiel", AnalyzeLineState.totalNumberOfBuses),
                    infoCard("Priemerná naplnenosť vozidiel", AnalyzeLineState.averageLoad + " cestujúcich"),
                    infoCard("Priemerná naplnenosť vozidiel", AnalyzeLineState.averageLoadInPercent + "%"),
                    spacing="5",
                    width="100%",
                    align_items="stretch",
                ),
                busStopChart("Priemerná naplnenosť naprieč zastávkami", AnalyzeLineState.loadPerBusStop, AnalyzeLineState.capacity, AnalyzeLineState.numberOfBusStops, AnalyzeLineState.longestBusStopNameLength),
                busStopChart("Priemerná naplnenosť naprieč zastávkami v percentách", AnalyzeLineState.loadInPercentPerBusStop, 100, AnalyzeLineState.numberOfBusStops, AnalyzeLineState.longestBusStopNameLength),
                spacing="5",
                width="100%",
            ),
        ),
        spacing="5",
        width="100%",
    ),