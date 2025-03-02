import reflex as rx
from datetime import datetime

from ..backend.models import TimeTable
from ..backend.InputParser import InputParser
from ..backend.Genetics import Genetics

from ..components.timeTable import timeTable
from ..components.infoCard import infoCard
from ..components.constraintInput import constraintInput

class OptimizeLineState(rx.State):
    selectedTimeTableName: str
    selectedTimeTable: str

    busSopsFilename: str = ""
    selectedBusStops: str = ""
    timeTableFilename: str = ""
    busStopTable: list[tuple[str, str, bool]] = []
    timeTable: list[tuple[str, str, bool]] = []

    currentGenerationBestTimeTable: list[tuple[str, str, bool]] = []
    bestTimeTable: list[tuple[str, str, bool]] = []
    bestTimeTableString: str = ""

    populationSize: int = 50
    mutationRate: float = 0.3
    elitismCount: int = 6
    constraints: list[int|None] = [None]*24
    numberOfGenerations: int = 100
    maxConnectionsPerHour: int = 15

    generationNumber: str = "0" + "/" + str(numberOfGenerations)

    optimizationRunning: bool = False
    _n_tasks: int = 0
    startTime: str = ''
    endTime: str = ''
    duration: str = ''

    showOptimization: bool = False

    saveTimeTableName: str = ""

    fitnessData = []
    maxFitnessX: int | None = None
    maxFitnessY: int | None = None

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
    async def resetOptimization(self):
        self.busSopsFilename = ""
        self.selectedBusStops = ""
        self.timeTableFilename = ""
        self.selectedTimeTable = ""
        self.selectedTimeTableName = ""
        self.busStopTable = []
        self.timeTable = []
        self.currentGenerationBestTimeTable = []
        self.bestTimeTable = []
        self.bestTimeTableString = ""

        self.populationSize = 50
        self.mutationRate = 0.3
        self.elitismCount = 6
        self.constraints = [None]*24
        self.numberOfGenerations = 100
        self.maxConnectionsPerHour = 15

        self.generationNumber = "0/" + str(self.numberOfGenerations)
        self.optimizationRunning = False
        self._n_tasks = 0
        self.startTime = ''
        self.endTime = ''
        self.duration = ''

        self.showOptimization = False

        self.saveTimeTableName = ""

        self.fitnessData = []
        self.maxFitnessX = None
        self.maxFitnessY = None

    @rx.event
    async def changeConstraints(self, val, hour: int) -> None:
        if val == "":
            self.constraints[hour] = None
        else:
            self.constraints[hour] = int(val)

    @rx.event(background=True)
    async def handle_optimize(self):
        async with self:
            if self._n_tasks > 0:
                return
            self._n_tasks += 1
            self.generationNumber = "0/" + str(self.numberOfGenerations)
            self.bestTimeTable = []
            self.currentGenerationBestTimeTable = []
            self.bestTimeTableString = ""
            self.fitnessData = []
            self.maxFitnessX = None
            self.maxFitnessY = None


        if not self.selectedBusStops:
            return

        busStops = InputParser.parseBusStopsFromString(self.selectedBusStops)

        if not self.selectedTimeTable:
            initialChromosome = None
        else:
            timeTable = InputParser.parseTimeTableFromString(self.selectedTimeTable)
            initialChromosome = timeTable.getChromosome()

        genetics = Genetics(self.populationSize, self.mutationRate, self.elitismCount, self.maxConnectionsPerHour, busStops, self.constraints, initialChromosome)

        for i in range(self.numberOfGenerations):
            timeTableTuple = self.parseTimeTableToTuple(TimeTable(genetics.generation[0].chromosome))
            bestTimeTableTuple = self.parseTimeTableToTuple(TimeTable(genetics.bestIndividual.chromosome))
            async with self:
                if not self.optimizationRunning:
                    break
                self.fitnessData.append({"generation": i+1, "fitness": genetics.generation[0].fitness})
                if self.maxFitnessY is None or self.maxFitnessY != genetics.bestIndividual.fitness:
                    self.maxFitnessX = i+1
                self.maxFitnessY = genetics.bestIndividual.fitness
                self.currentGenerationBestTimeTable = timeTableTuple
                self.bestTimeTable = bestTimeTableTuple
                self.bestTimeTableString = str(TimeTable(genetics.bestIndividual.chromosome))
                self.generationNumber = str(i+1) + "/" + str(self.numberOfGenerations)
            genetics.updateGeneration()
                
        async with self:
            self.optimizationRunning = False
            self._n_tasks -= 1
            self.endTime = datetime.now().strftime("%H:%M:%S")
            self.duration = str(datetime.strptime(self.endTime, "%H:%M:%S") - datetime.strptime(self.startTime, "%H:%M:%S"))
            yield rx.toast.success("Optimalizácia dokončená")

    @rx.event
    async def toggle_optimization_run(self):
        self.optimizationRunning = not self.optimizationRunning
        if self.optimizationRunning:
            self.startTime = datetime.now().strftime("%H:%M:%S")
            self.showOptimization = True
            return OptimizeLineState.handle_optimize
        
    def initConstraints(self):
        busStops = InputParser.parseBusStopsFromString(self.selectedBusStops)
        busStopRates = {rate[0] for busStop in busStops for rate in busStop.passengerArrivalRatesPerHour}
        self.constraints = [0 if hour not in busStopRates else self.constraints[hour] for hour in range(24)]
        
    @rx.event
    async def saveTimeTable(self):
        from ..components.infoUpload import InfoUploadState
        state = await self.get_state(InfoUploadState)
        if self.saveTimeTableName == "":
            self.saveTimeTableName = "Rozpis " + str(datetime.now())
        state.insertNewTimeTable((self.saveTimeTableName, self.bestTimeTableString))
        self.saveTimeTableName = ""

def optimizeLine() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.vstack(
                rx.text("Veľkosť populácie"),
                rx.input(
                    placeholder="Veľkosť populácie",
                    value=OptimizeLineState.populationSize,
                    on_change=OptimizeLineState.set_populationSize,
                    width="100%",
                    size="3",
                    min="1",
                    type="number",
                    color_scheme=rx.cond(
                        OptimizeLineState.populationSize < 1,
                        "red",
                        "dark"
                    ),
                    variant=rx.cond(
                        OptimizeLineState.populationSize < 1,
                        "soft",
                        "classic"
                    ),
                    disabled=rx.cond(
                        OptimizeLineState.optimizationRunning,
                        True,
                        False,
                    ),
                ),
                width="100%",
                justify="between",
            ),
            rx.vstack(
                rx.text("Počet generácií"),
                rx.input(
                    placeholder="Počet generácií",
                    value=OptimizeLineState.numberOfGenerations,
                    on_change=OptimizeLineState.set_numberOfGenerations,
                    width="100%",
                    size="3",
                    min="1",
                    type="number",
                    color_scheme=rx.cond(
                        OptimizeLineState.numberOfGenerations < 1,
                        "red",
                        "dark"
                    ),
                    variant=rx.cond(
                        OptimizeLineState.numberOfGenerations < 1,
                        "soft",
                        "classic"
                    ),
                    disabled=rx.cond(
                        OptimizeLineState.optimizationRunning,
                        True,
                        False,
                    ),
                ),
                width="100%",
                justify="between",
            ),
            rx.vstack(
                rx.text("Pravdepodobnosť mutácie"),
                rx.input(
                    placeholder="Pravdepodobnosť mutácie",
                    value=OptimizeLineState.mutationRate,
                    on_change=OptimizeLineState.set_mutationRate,
                    width="100%",
                    size="3",
                    min="0",
                    max="1",
                    type="number",
                    color_scheme=rx.cond(
                        (OptimizeLineState.mutationRate < 0) | (OptimizeLineState.mutationRate > 1),
                        "red",
                        "dark"
                    ),
                    variant=rx.cond(
                        (OptimizeLineState.mutationRate < 0) | (OptimizeLineState.mutationRate > 1),
                        "soft",
                        "classic"
                    ),
                    disabled=rx.cond(
                        OptimizeLineState.optimizationRunning,
                        True,
                        False,
                    ),
                ),
                width="100%",
                justify="between",
            ),
            rx.vstack(
                rx.text("Elitizmus"),
                rx.input(
                    placeholder="Elitizmus",
                    value=OptimizeLineState.elitismCount,
                    on_change=OptimizeLineState.set_elitismCount,
                    width="100%",
                    size="3",
                    min="0",
                    type="number",
                    color_scheme=rx.cond(
                        OptimizeLineState.elitismCount < 0,
                        "red",
                        "dark"
                    ),
                    variant=rx.cond(
                        OptimizeLineState.elitismCount < 0,
                        "soft",
                        "classic"
                    ),
                    disabled=rx.cond(
                        OptimizeLineState.optimizationRunning,
                        True,
                        False,
                    ),
                ),
                width="100%",
                justify="between",
            ),
            rx.vstack(
                rx.text("Maximálny počet spojov za hodinu"),
                rx.input(
                    placeholder="Maximálny počet spojov za hodinu",
                    value=OptimizeLineState.maxConnectionsPerHour,
                    on_change=OptimizeLineState.set_maxConnectionsPerHour,
                    width="100%",
                    size="3",
                    min="0",
                    type="number",
                    color_scheme=rx.cond(
                        OptimizeLineState.maxConnectionsPerHour < 1,
                        "red",
                        "dark"
                    ),
                    variant=rx.cond(
                        OptimizeLineState.maxConnectionsPerHour < 1,
                        "soft",
                        "classic"
                    ),
                    disabled=rx.cond(
                        OptimizeLineState.optimizationRunning,
                        True,
                        False,
                    ),
                ),
                width="100%",
                justify="between",
            ),
            width="100%",
            spacing="5",
            align="stretch",
        ),
        constraintInput(),
        rx.hstack(
            rx.button(
                rx.heading("Resetovať", size="3"),
                on_click=[
                    OptimizeLineState.resetOptimization(),
                    rx.toast.info("Optimalizácia resetovaná"),
                ],
                size="3",
            ),
            rx.button(
                rx.heading(rx.cond(OptimizeLineState.optimizationRunning, "Zastaviť", "Optimalizovať"), size="3"),
                on_click=[
                    OptimizeLineState.toggle_optimization_run(),
                    rx.cond(OptimizeLineState.optimizationRunning, rx.toast.info("Optimalizácia zastavená"), rx.toast.info("Optimalizácia spustená")),
                ],
                size="3",
                disabled=rx.cond(
                    (OptimizeLineState.selectedBusStops == ""),
                    True,
                    False,
                ),
            ),
            width="100%",
            justify="center",
        ),
        rx.cond(
            OptimizeLineState.showOptimization,
            rx.vstack(
                rx.hstack(
                    rx.heading("Optimalizácia", size="8"),
                    padding_y="1em",
                    width="100%",
                    justify="center",
                ),
                rx.hstack(
                    infoCard("Generácia", OptimizeLineState.generationNumber),
                    infoCard("Začiatok", OptimizeLineState.startTime),
                    infoCard("Koniec", OptimizeLineState.endTime, loading=rx.cond(OptimizeLineState.optimizationRunning, True, False)),
                    infoCard("Trvanie", OptimizeLineState.duration, loading=rx.cond(OptimizeLineState.optimizationRunning, True, False)),
                    width="100%",
                    spacing="5",
                    align="stretch",
                ),
                rx.card(
                    rx.vstack(
                        rx.heading("Fitness funkcia", size="4"),
                        rx.recharts.line_chart(
                            rx.recharts.line(
                                data_key="fitness",
                                dot=False,
                            ),
                            rx.recharts.reference_dot(
                                x=OptimizeLineState.maxFitnessX,
                                y=OptimizeLineState.maxFitnessY,
                                r=5,    
                            ),
                            rx.recharts.x_axis(data_key="generation",  domain=[0, OptimizeLineState.numberOfGenerations]),
                            rx.recharts.y_axis(),
                            rx.recharts.graphing_tooltip(),
                            data=OptimizeLineState.fitnessData,
                            
                            width="100%",
                            height=300,
                        ),
                        align_items="center",
                    ),
                    size="3",
                    width="100%",
                ),
                rx.hstack(
                    rx.vstack(
                        rx.cond(
                            OptimizeLineState.currentGenerationBestTimeTable,
                            rx.vstack(
                                timeTable(OptimizeLineState.currentGenerationBestTimeTable, "Najlepší rozpis v generácii"),
                            ),
                            rx.text("\u00A0"),
                            
                        ),
                        align_items="end",
                        flex="1",
                    ),
                    rx.vstack(
                        rx.cond(
                            OptimizeLineState.bestTimeTable,
                            rx.vstack(
                                timeTable(OptimizeLineState.bestTimeTable, "Najlepší rozpis celkovo"),
                                rx.vstack(
                                    rx.text("Názov rozpisu"),
                                    rx.input(
                                        placeholder="Názov rozpisu",
                                        value=OptimizeLineState.saveTimeTableName,
                                        on_change=OptimizeLineState.set_saveTimeTableName,
                                        width="100%",
                                        size="3",
                                        type="text",
                                        disabled=rx.cond(
                                            OptimizeLineState.optimizationRunning,
                                            True,
                                            False,
                                        ),
                                    ),
                                    width="100%"
                                ),
                                rx.button(
                                    rx.heading("Uložiť najlepší rozpis", size="3"),
                                    on_click=[
                                        OptimizeLineState.saveTimeTable(),
                                        rx.toast.success("Rozpis bol uložený"),
                                    ],
                                    disabled=rx.cond(
                                        OptimizeLineState.optimizationRunning,
                                        True,
                                        False,
                                    ),
                                    size="3",
                                    width="100%",
                                ),
                            ),
                            rx.text("\u00A0"),
                        ),
                        flex="1",
                    ),
                    spacing="5",
                    width="100%",
                ),        
                width="100%",
                spacing="5",
            ),
        ),
        spacing="5",
        width="100%",
    ),