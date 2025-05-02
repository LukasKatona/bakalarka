"""
This file contains analyze line component and its state.
"""

import reflex as rx
from tkinter import filedialog

from ..backend.InputParser import InputParser
from ..backend.Simulation import Simulation

from .infoCard import infoCard
from .hourChart import hourChart
from .busStopChart import busStopChart
from .numberInput import numberImput

class AnalyzeLineState(rx.State):
    selectedTimeTableName: str = ""
    selectedTimeTable: str = ""

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
    totalPassengersLeftUnboarded: str = ""
    totalTimeSpentWaiting: str = ""
    averageTimeSpentWaiting: str = ""
    passengersArrivedPerHour: list[dict[str,int]] = []
    passengersLeftUnboardedPerHour: list[dict[str,int]] = []
    timeSpentWaitingPerHour: list[dict[str,int]] = []

    vehicleCapacity: int = 80
    vehicleSeats: int = 30
    costPerSeatKm: float = 99.82
    routeLength: float = 3.8

    averageLoad: str = ""
    averageLoadInPercent: str = ""
    totalPassengersTransported: int
    averagePassengerSatisfaction: str = ""
    loadPerBusStop: list[dict[str,int]] = []

    totalCost: str = ""

    showAnalysis: bool = False

    @rx.event
    async def resetAnalysis(self):
        """
        Resets all state variables.
        """
        self.selectedTimeTableName = ""
        self.selectedTimeTable = ""

        self.busSopsFilename = ""
        self.selectedBusStops = ""
        self.timeTableFilename = ""
        self.busStopTable = []
        self.timeTable = []
        
        self.numberOfBusStops = 0
        self.longestBusStopNameLength = 0

        self.totalNumberOfBuses = 0
        self.totalPassengersArrived = 0
        self.totalPassengersDeparted = 0
        self.totalPassengersLeftUnboarded = ""
        self.totalTimeSpentWaiting = ""
        self.averageTimeSpentWaiting= ""
        self.passengersArrivedPerHour = []
        self.passengersLeftUnboardedPerHour = []
        self.timeSpentWaitingPerHour = []

        self.vehicleCapacity = 80
        self.vehicleSeats = 30
        self.costPerSeatKm= 99.82
        self.routeLength = 3.8

        self.averageLoad = ""
        self.averageLoadInPercent  = ""
        self.totalPassengersTransported = 0
        self.averagePassengerSatisfaction = ""
        self.loadPerBusStop = []

        self.totalCost = ""

        self.showAnalysis = False


    @rx.event
    async def handleAnalysis(self):
        """
        Handles whole analysis process.
        """
        if not self.selectedBusStops or not self.selectedTimeTable:
            return

        busStops = InputParser.parseBusStopsFromString(self.selectedBusStops)
        timeTable = InputParser.parseTimeTableFromString(self.selectedTimeTable)
        stats = Simulation.runMultipleThanAverage(0, 24*60, busStops, timeTable, self.vehicleCapacity, self.vehicleSeats, 10)

        self.numberOfBusStops = len(busStops)
        self.longestBusStopNameLength = max([len(busStop.name) for busStop in busStops])

        self.totalNumberOfBuses = int(stats.totalNumberOfBuses)

        self.totalPassengersArrived = stats.busStopStatistics.totalPassengersArrived
        self.totalPassengersDeparted = stats.busStopStatistics.totalPassengersDeparted
        self.totalPassengersLeftUnboarded = str(stats.busStopStatistics.totalPassengersLeftUnboarded) + " (" + str(round(stats.busStopStatistics.totalPassengersLeftUnboarded / stats.busStopStatistics.totalPassengersArrived * 100, 2)) + "%)"
        self.totalTimeSpentWaiting = str(int(round(stats.busStopStatistics.totalTimeSpentWaiting)))
        self.averageTimeSpentWaiting = str(int(round(stats.busStopStatistics.totalTimeSpentWaiting / stats.busStopStatistics.totalPassengersArrived)))

        self.passengersArrivedPerHour = [{"hour": hour, "count": 0} for hour in range(24)]
        for stat in stats.busStopStatistics.passengersArrivedPerHour:
            self.passengersArrivedPerHour[int(stat[0])]["count"] = stat[1]

        self.passengersLeftUnboardedPerHour = [{"hour": hour, "count": 0} for hour in range(24)]
        for stat in stats.busStopStatistics.passengersLeftUnboardedPerHour:
            self.passengersLeftUnboardedPerHour[int(stat[0])]["count"] = stat[1]

        self.timeSpentWaitingPerHour = [{"hour": hour, "count": 0} for hour in range(24)]
        for stat in stats.busStopStatistics.timeSpentWaitingPerHour:
            passengerArrivedCount = next((arrivedStat[1] for arrivedStat in stats.busStopStatistics.passengersArrivedPerHour if arrivedStat[0] == stat[0]),1)
            self.timeSpentWaitingPerHour[int(stat[0])]["count"] = stat[1] / passengerArrivedCount

        self.averageLoad = str(int(round(stats.busStatistics.averageLoad)))
        self.averageLoadInPercent = str(round(stats.busStatistics.averageLoadInPercent*100, 2))
        self.totalPassengersTransported = stats.busStatistics.totalPassengersTransported
        self.averagePassengerSatisfaction = str(round(stats.averagePassengerSatisfaction*100, 2))

        self.loadPerBusStop = []
        for stat in stats.busStatistics.loadPerBusStop:
            name = stat[0].replace(" ", "\u00A0")
            self.loadPerBusStop.append({"name": name, "load": int(round(stat[1]))})

        self.totalCost = str(int(round(self.routeLength * self.totalNumberOfBuses * self.vehicleCapacity / 100 * self.costPerSeatKm)))

        self.showAnalysis = True

    @rx.event
    async def handleExport(self):
        """
        Handles export of the analysis to txt file.
        """
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Uložiť analýzu",
        )
        if file_path:
            with open(file_path, 'w') as file:
                file.write(
                    f"Analýza linky\n"
                    f"\n------- Zastávky -------\n"
                )
                for busStop in InputParser.parseBusStopsFromString(self.selectedBusStops):
                    file.write(
                        f"{busStop}\n"
                    )
                file.write(
                    f"\n------- Časový rozpis -------\n"
                    f"{InputParser.parseTimeTableFromString(self.selectedTimeTable)}\n\n"
                    f"------- Vstupy -------\n"
                    f"Kapacita vozidla: {self.vehicleCapacity}\n"
                    f"Počet miest na sedenie: {self.vehicleSeats}\n"
                    f"Celkové náklady (Kč/100 miesto-km): {self.costPerSeatKm} Kč\n"
                    f"Dĺžka trasy: {self.routeLength} km\n"
                    f"\n------- Výstupy -------\n"
                    f"Počet príchodov cestujúcich: {self.totalPassengersArrived}\n"
                    f"Počet prevezených cestujúcich: {self.totalPassengersTransported}\n"
                    f"Počet neobslúžených cestujúcich: {self.totalPassengersLeftUnboarded}\n"
                    f"Celkový čas strávený čakaním: {self.totalTimeSpentWaiting} min\n"
                    f"Priemerný čas strávený čakaním: {self.averageTimeSpentWaiting} min\n"
                    f"Celkové náklady: {self.totalCost} Kč\n"
                    f"Priemerná spokojnosť cestujúcich: {self.averagePassengerSatisfaction} %\n"
                    f"Celkový počet vozidiel: {self.totalNumberOfBuses}\n"
                    f"Priemerná naplnenosť vozidiel: {self.averageLoad} ({self.averageLoadInPercent} %)\n"
                    f"Cestujúci prichádzajúci za hodinu:\n{self.passengersArrivedPerHour}\n"
                    f"Priemerný čas strávený čakaním za hodinu (min):\n{self.timeSpentWaitingPerHour}\n"
                    f"Počet prípadov kedy sa cestujúci nezmestili do vozidla za hodinu:\n{self.passengersLeftUnboardedPerHour}\n"
                    f"Priemerná naplnenosť vozidiel naprieč zastávkami:\n{self.loadPerBusStop}\n"
                )


def analyzeLine() -> rx.Component:
    """
    Analyze line component, contains all number inputs, and analysis results with option to save the results as txt file.

    :return: Analyze line component
    :rtype: rx.Component
    """
    return rx.vstack(
        rx.hstack(
            numberImput("Kapacita vozidla", "Kapacita vozidla", AnalyzeLineState.vehicleCapacity, AnalyzeLineState.set_vehicleCapacity, "1", None, AnalyzeLineState.vehicleCapacity < 1),
            numberImput("Miest na sedenie", "Miest na sedenie", AnalyzeLineState.vehicleSeats, AnalyzeLineState.set_vehicleSeats, "0", None, AnalyzeLineState.vehicleSeats < 0),
            numberImput("Celkové náklady (Kč/100 miesto-km)", "Kč/100 miesto-km", AnalyzeLineState.costPerSeatKm, AnalyzeLineState.set_costPerSeatKm, "0", None, AnalyzeLineState.costPerSeatKm < 0),
            numberImput("Dĺžka trasy", "Dĺžka trasy", AnalyzeLineState.routeLength, AnalyzeLineState.set_routeLength, "0", None, AnalyzeLineState.routeLength < 0),
            width="100%",
            spacing="5",
            align="stretch",
        ),
        rx.hstack(
            rx.button(
                rx.heading("Resetovať", size="3"),
                on_click=AnalyzeLineState.resetAnalysis(),
                size="3",
            ),
            rx.button(
                rx.heading("Analyzovať", size="3"),
                on_click=AnalyzeLineState.handleAnalysis(),
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
                    infoCard("Počet príchodov cestujúcich", AnalyzeLineState.totalPassengersArrived),
                    infoCard("Počet prevezených cestujúcich", AnalyzeLineState.totalPassengersTransported),
                    infoCard("Počet neobslúžených cestujúcich", AnalyzeLineState.totalPassengersLeftUnboarded),
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
                    infoCard("Celkové náklady", AnalyzeLineState.totalCost + " Kč"),
                    infoCard("Priemerná spokojnosť cestujúcich", AnalyzeLineState.averagePassengerSatisfaction + "%"),
                    spacing="5",
                    width="100%",
                    align_items="stretch",
                ),
                rx.hstack(
                    infoCard("Celkový počet vozidiel", AnalyzeLineState.totalNumberOfBuses),
                    infoCard("Priemerná naplnenosť vozidiel", AnalyzeLineState.averageLoad + " cestujúcich (" + AnalyzeLineState.averageLoadInPercent + "%)"),
                    spacing="5",
                    width="100%",
                    align_items="stretch",
                ),
                hourChart("Cestujúci prichádzajúci za hodinu", AnalyzeLineState.passengersArrivedPerHour),
                hourChart("Priemerný čas strávený čakaním za hodinu (min)", AnalyzeLineState.timeSpentWaitingPerHour),
                hourChart("Počet prípadov kedy sa cestujúci nezmestil do vozidla za hodinu", AnalyzeLineState.passengersLeftUnboardedPerHour),
                busStopChart("Priemerná naplnenosť naprieč zastávkami", AnalyzeLineState.loadPerBusStop, AnalyzeLineState.vehicleCapacity, AnalyzeLineState.numberOfBusStops, AnalyzeLineState.longestBusStopNameLength),
                rx.button(
                    rx.heading("Uložiť analýzu", size="3"),
                    on_click=AnalyzeLineState.handleExport(),
                    size="3",
                ),
                spacing="5",
                width="100%",
                align="center",
            ),
        ),
        spacing="5",
        width="100%",
    ),