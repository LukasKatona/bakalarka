import reflex as rx
from datetime import datetime

from ..backend.models import TimeTable
from ..backend.InputParser import InputParser
from ..backend.Genetics import Genetics

class OptimizeLineState(rx.State):
    bus_sops_filename: str = ""
    bus_stops_filecontent: str = ""
    time_table_filename: str = ""
    time_table_filecontent: str = ""
    busStopTable: list[tuple[str, str, bool]] = []
    timeTable: list[tuple[str, str, bool]] = []

    populationSize: int = 10
    mutationRate: float = 0.3
    elitismCount: int = 2
    constraints = [0,0,0,0,0,'x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x',0]
    #constraints = ['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x']
    numberOfGenerations: int = 5

    generationNumber: int = 0

    optimizationRunning: bool = False
    _n_tasks: int = 0
    startTime: int = 0
    endTime: int = 0
    duration: int = 0

    def parseTimeTableToTuple(self, timeTable: TimeTable) -> list[tuple[str, str, bool]]:
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
    async def clear_files(self):
        self.bus_sops_filename = ""
        self.bus_stops_filecontent = ""
        self.time_table_filename = ""
        self.time_table_filecontent = ""
        self.busStopTable = []
        self.timeTable = []

        self.generationNumber = 0
        self.optimizationRunning = False
        self._n_tasks = 0
        self.startTime = 0
        self.endTime = 0
        self.duration = 0

    @rx.event(background=True)
    async def handle_optimize(self):
        async with self:
            if self._n_tasks > 0:
                return
            self._n_tasks += 1

        if not self.bus_stops_filecontent:
            return

        busStops = InputParser.parseBusStopsFromString(self.bus_stops_filecontent)

        if not self.time_table_filecontent:
            initialChromosome = None
        else:
            timeTable = InputParser.parseTimeTableFromString(self.time_table_filecontent)
            initialChromosome = timeTable.getChromosome()

        genetics = Genetics(self.populationSize, self.mutationRate, self.elitismCount, busStops, self.constraints, initialChromosome)

        lastChromosomes = []
        for i in range(self.numberOfGenerations):
            genetics.updateGeneration()
            lastChromosomes.append(genetics.generation[0].chromosome)
            timeTableTuple = self.parseTimeTableToTuple(TimeTable(genetics.generation[0].chromosome))

            async with self:
                self.timeTable = timeTableTuple
                self.generationNumber = i
                if len(lastChromosomes) == 5:
                    if lastChromosomes[0] == lastChromosomes[1] == lastChromosomes[2] == lastChromosomes[3] == lastChromosomes[4]:
                        self.optimizationRunning = False
                    lastChromosomes.pop(0)
                if not self.optimizationRunning:
                    break
                
        async with self:
            self._n_tasks -= 1
            self.endTime = datetime.now().timestamp()
            self.duration = self.endTime - self.startTime


    @rx.event
    async def toggle_optimization_run(self):
        self.optimizationRunning = not self.optimizationRunning
        if self.optimizationRunning:
            self.startTime = datetime.now().timestamp()
            return OptimizeLineState.handle_optimize

def optimizeLine() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.button(
                rx.heading("Vymazať súbory"),
                on_click=OptimizeLineState.clear_files(),
                size="4",
            ),
            rx.button(
                rx.cond(OptimizeLineState.optimizationRunning, rx.heading("Zastaviť"), rx.heading("Optimalizovať")),
                on_click=OptimizeLineState.toggle_optimization_run(),
                size="4",
                disabled=rx.cond(
                    (OptimizeLineState.bus_stops_filecontent == ""),
                    True,
                    False,
                ),
            ),
            width="100%",
            justify="center",
        ),
        rx.text(OptimizeLineState.generationNumber),
        rx.text(OptimizeLineState.optimizationRunning),
        rx.text(OptimizeLineState.startTime),
        rx.text(OptimizeLineState.endTime),
        rx.text(OptimizeLineState.duration),
        spacing="5",
        width="100%",
    ),