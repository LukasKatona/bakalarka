import reflex as rx
from datetime import datetime

from ..backend.models import TimeTable
from ..backend.InputParser import InputParser
from ..backend.Genetics import Genetics

from ..components.timeTable import timeTable

class OptimizeLineState(rx.State):
    selectedTimeTableName: str
    selectedTimeTable: str

    busSopsFilename: str = ""
    selectedBusStops: str = ""
    timeTableFilename: str = ""
    busStopTable: list[tuple[str, str, bool]] = []
    timeTable: list[tuple[str, str, bool]] = []

    bestTimeTable: list[tuple[str, str, bool]] = []
    bestTimeTableString: str = ""

    populationSize: int = 50
    mutationRate: float = 0.3
    elitismCount: int = 6
    constraints = [0,0,0,0,0,'x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x',0]
    #constraints = ['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x']
    numberOfGenerations: int = 100

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
        self.busSopsFilename = ""
        self.selectedBusStops = ""
        self.timeTableFilename = ""
        self.selectedTimeTable = ""
        self.selectedTimeTableName = ""
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

        if not self.selectedBusStops:
            return

        busStops = InputParser.parseBusStopsFromString(self.selectedBusStops)

        if not self.selectedTimeTable:
            initialChromosome = None
        else:
            timeTable = InputParser.parseTimeTableFromString(self.selectedTimeTable)
            initialChromosome = timeTable.getChromosome()

        genetics = Genetics(self.populationSize, self.mutationRate, self.elitismCount, busStops, self.constraints, initialChromosome)

        lastChromosomes = []
        for i in range(self.numberOfGenerations):
            time = datetime.now().timestamp()
            genetics.updateGeneration()
            print("time to update generation: ", datetime.now().timestamp() - time)
            lastChromosomes.append(genetics.generation[0].chromosome)
            timeTableTuple = self.parseTimeTableToTuple(TimeTable(genetics.generation[0].chromosome))
            bestTimeTableTuple = self.parseTimeTableToTuple(TimeTable(genetics.bestIndividual.chromosome))
            print(genetics)
            async with self:
                self.timeTable = timeTableTuple
                self.bestTimeTable = bestTimeTableTuple
                self.bestTimeTableString = str(TimeTable(genetics.generation[0].chromosome))
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
        
    @rx.event
    async def saveTimeTableToDropdown(self):
        print("saving")
        from ..components.infoUpload import InfoUploadState
        state = await self.get_state(InfoUploadState)
        state.insertNewTimeTable((str(datetime.now()), self.bestTimeTableString))

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
                    (OptimizeLineState.selectedBusStops == ""),
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
        timeTable(OptimizeLineState.bestTimeTable),
        rx.button(
            rx.heading("Uložiť do dropdownu"),
            on_click=OptimizeLineState.saveTimeTableToDropdown(),
        ),
        spacing="5",
        width="100%",
    ),