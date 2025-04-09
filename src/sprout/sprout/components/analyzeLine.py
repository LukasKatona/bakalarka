import reflex as rx
import tkinter as tk
from tkinter import filedialog

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
    passengersLeftUnboardedPerHour = []
    timeSpentWaitingPerHour = []

    vehicleCapacity: int = 80
    vehicleSeats: int = 30
    vehiclePriceCompensation: float = 66.35
    routeLength: float = 3.8
    pricePerTicket: int = 25

    averageLoad: str
    averageLoadInPercent: str
    totalPassengersTransported: int
    averagePassengerSatisfaction: str
    loadPerBusStop = []

    totalCompensation: str
    totalProfit: str

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
        self.vehiclePriceCompensation = 66.35
        self.routeLength = 3.8
        self.pricePerTicket = 25

    @rx.event
    async def handle_analyze(self):
        if not self.selectedBusStops or not self.selectedTimeTable:
            return

        busStops = InputParser.parseBusStopsFromString(self.selectedBusStops)
        timeTable = InputParser.parseTimeTableFromString(self.selectedTimeTable)
        stats = Simulation.runMultipleThanAverage(0, 24*60, busStops, timeTable, self.vehicleCapacity, self.vehicleSeats, 30)

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
            passengerArrivedStat = [x for x in stats.busStopStatistics.passengersArrivedPerHour if x[0] == stat[0]]
            if passengerArrivedStat[0][1] > 0:
                self.timeSpentWaitingPerHour[int(stat[0])]["count"] = stat[1] / passengerArrivedStat[0][1]

        self.averageLoad = str(int(round(stats.busStatistics.averageLoad)))
        self.averageLoadInPercent = str(round(stats.busStatistics.averageLoadInPercent*100, 2))
        self.totalPassengersTransported = stats.busStatistics.totalPassengersTransported
        self.averagePassengerSatisfaction = str(round(stats.averagePassengerSatisfaction*100, 2))

        self.loadPerBusStop = []
        for stat in stats.busStatistics.loadPerBusStop:
            name = stat[0].replace(" ", "\u00A0")
            self.loadPerBusStop.append({"name": name, "load": int(round(stat[1]))})

        totalCompensation = (self.routeLength * self.totalNumberOfBuses * self.vehicleCapacity / 100 * self.vehiclePriceCompensation)
        self.totalProfit = str(int(round(- totalCompensation + self.pricePerTicket * self.totalPassengersTransported)))
        self.totalCompensation = str(int(round(-totalCompensation)))

        self.showAnalysis = True

    @rx.event
    async def handle_export(self):
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
                    f"Kompenzácia vozidla: {self.vehiclePriceCompensation} Kč\n"
                    f"Dĺžka trasy: {self.routeLength} km\n"
                    f"Cena lístka: {self.pricePerTicket} Kč\n"
                    f"\n------- Výstupy -------\n"
                    f"Počet príchodov cestujúcich: {self.totalPassengersArrived}\n"
                    f"Počet prevezených cestujúcich: {self.totalPassengersTransported}\n"
                    f"Počet neobslúžených cestujúcich: {self.totalPassengersLeftUnboarded}\n"
                    f"Celkový čas strávený čakaním: {self.totalTimeSpentWaiting} min\n"
                    f"Priemerný čas strávený čakaním: {self.averageTimeSpentWaiting} min\n"
                    f"Celková kompenzácia: {self.totalCompensation} Kč\n"
                    f"Celkový zisk: {self.totalProfit} Kč\n"
                    f"Priemerná spokojnosť cestujúcich: {self.averagePassengerSatisfaction} %\n"
                    f"Celkový počet vozidiel: {self.totalNumberOfBuses}\n"
                    f"Priemerná naplnenosť vozidiel: {self.averageLoad} ({self.averageLoadInPercent} %)\n"
                    f"Cestujúci prichádzajúci za hodinu:\n{self.passengersArrivedPerHour}\n"
                    f"Priemerný čas strávený čakaním za hodinu (min):\n{self.timeSpentWaitingPerHour}\n"
                    f"Počet prípadov kedy sa cestujúci nezmestili do vozidla za hodinu:\n{self.passengersLeftUnboardedPerHour}\n"
                    f"Priemerná naplnenosť vozidiel naprieč zastávkami:\n{self.loadPerBusStop}\n"
                )


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
            rx.vstack(
                rx.text("Kompenzácia vozidla"),
                rx.input(
                    placeholder="Kompenzácia vozidla",
                    value=AnalyzeLineState.vehiclePriceCompensation,
                    on_change=AnalyzeLineState.set_vehiclePriceCompensation,
                    width="100%",
                    size="3",
                    min="0",
                    type="number",
                    color_scheme=rx.cond(
                        AnalyzeLineState.vehiclePriceCompensation < 0,
                        "red",
                        "dark"
                    ),
                    variant=rx.cond(
                        AnalyzeLineState.vehiclePriceCompensation < 0,
                        "soft",
                        "classic"
                    ),
                ),
                width="100%",
                justify="between",
            ),
            rx.vstack(
                rx.text("Dĺžka trasy"),
                rx.input(
                    placeholder="Dĺžka trasy",
                    value=AnalyzeLineState.routeLength,
                    on_change=AnalyzeLineState.set_routeLength,
                    width="100%",
                    size="3",
                    min="0",
                    type="number",
                    color_scheme=rx.cond(
                        AnalyzeLineState.routeLength < 0,
                        "red",
                        "dark"
                    ),
                    variant=rx.cond(
                        AnalyzeLineState.routeLength < 0,
                        "soft",
                        "classic"
                    ),
                ),
                width="100%",
                justify="between",
            ),
            rx.vstack(
                rx.text("Cena lístka"),
                rx.input(
                    placeholder="Cena lístka",
                    value=AnalyzeLineState.pricePerTicket,
                    on_change=AnalyzeLineState.set_pricePerTicket,
                    width="100%",
                    size="3",
                    min="0",
                    type="number",
                    color_scheme=rx.cond(
                        AnalyzeLineState.pricePerTicket < 0,
                        "red",
                        "dark"
                    ),
                    variant=rx.cond(
                        AnalyzeLineState.pricePerTicket < 0,
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
                    infoCard("Celková kompenzácia", AnalyzeLineState.totalCompensation + " Kč"),
                    infoCard("Celkový zisk", AnalyzeLineState.totalProfit + " Kč"),
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
                    on_click=AnalyzeLineState.handle_export(),
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