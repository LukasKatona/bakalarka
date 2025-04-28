import reflex as rx
from datetime import datetime

from ..backend.models import TimeTable
from ..backend.InputParser import InputParser
from ..backend.Genetics import Genetics

from ..components.timeTable import timeTable
from ..components.infoCard import infoCard
from ..components.constraintInput import constraintInput
from .numberInput import numberImput

class OptimizeLineState(rx.State):
    selectedTimeTableName: str
    selectedTimeTable: str

    busSopsFilename: str = ""
    selectedBusStops: str = ""
    timeTableFilename: str = ""
    busStopTable: list[tuple[str, str, bool]] = []
    timeTable: list[tuple[str, str, bool]] = []

    populationSize: int = 50
    sliderMax: int = populationSize - 1
    mutationRate: float = 0.05
    constraints: list[int|None] = [None]*24
    numberOfGenerations: int = 100
    maxConnectionsPerHour: int = 15
    vehicleCapacity: int = 80
    vehicleSeats: int = 30
    costPerSeatKm: float = 99.82
    routeLength: float = 3.8
    

    generationNumber: str = "0" + "/" + str(numberOfGenerations)

    optimizationRunning: bool = False
    _n_tasks: int = 0
    startTime: str = ''
    endTime: str = ''
    duration: str = ''

    generation = []
    generationChromosomes: list[list[int]] = []
    selectedChromosomeIndex: int
    selectedScatterPoint = {}

    showOptimization: bool = False

    bestTimeTable: list[tuple[str, str, bool]] = []
    bestTimeTableString: str = ""
    bestTimeTableChromosome: list[int] = []
    saveTimeTableName: str = ""

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
        self.busStopTable = []
        self.timeTable = []

        self.populationSize = 50
        self.sliderMax = self.populationSize - 1
        self.mutationRate = 0.05
        self.constraints = [None]*24
        self.numberOfGenerations = 100
        self.maxConnectionsPerHour = 15
        self.vehicleCapacity = 80
        self.vehicleSeats = 30
        self.costPerSeatKm = 99.82
        self.routeLength = 3.8

        self.generationNumber = "0/" + str(self.numberOfGenerations)
        self.optimizationRunning = False
        self._n_tasks = 0
        self.startTime = ''
        self.endTime = ''
        self.duration = ''

        self.generation = []
        self.generationChromosomes = []
        self.selectedChromosomeIndex = int(round(self.numberOfGenerations / 2))
        selectedScatterPoint = {}

        self.showOptimization = False

        self.saveTimeTableName = ""
        self.bestTimeTable = []
        self.bestTimeTableString = ""

    @rx.event
    async def changeConstraints(self, val, hour: int) -> None:
        if val == "":
            self.constraints[hour] = None
        else:
            self.constraints[hour] = int(val)

    @rx.event(background=True)
    async def handle_optimize(self):
        if not self.selectedBusStops:
            return
        
        async with self:
            if self._n_tasks > 0:
                return
            self._n_tasks += 1
            self.generationNumber = "0/" + str(self.numberOfGenerations)

        genetics = Genetics(self.populationSize, self.mutationRate, self.maxConnectionsPerHour, self.vehicleCapacity, self.vehicleSeats, self.costPerSeatKm, self.routeLength, InputParser.parseBusStopsFromString(self.selectedBusStops), self.constraints)

        for i in range(self.numberOfGenerations):
            async with self:
                if not self.optimizationRunning:
                    break
                self.generationNumber = str(i+1) + "/" + str(self.numberOfGenerations)
                self.generation = []
                self.generationChromosomes = []
                sortedGeneration = genetics.generation.copy()
                sortedGeneration = sorted(sortedGeneration, key=lambda individual: individual.cost)
                for individual in sortedGeneration:
                    self.generation.append({"cost": individual.cost, "satisfaction": individual.satisfaction})
                    self.generationChromosomes.append(individual.chromosome)
                self.bestTimeTableChromosome = genetics.generation[int(round(len(genetics.generation)/2))].chromosome
                self.bestTimeTableString = str(TimeTable(self.bestTimeTableChromosome))
                self.bestTimeTable = self.parseTimeTableToTuple(TimeTable(self.bestTimeTableChromosome))
                if i == 0 or i == self.numberOfGenerations - 1:
                    print(self.generation)
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
    def setTimeTable(self, value):
        self.selectedChromosomeIndex = value[0]
        self.bestTimeTableChromosome = self.generationChromosomes[self.selectedChromosomeIndex]
        self.selectedScatterPoint = self.generation[self.selectedChromosomeIndex]
        self.bestTimeTableString = str(TimeTable(self.bestTimeTableChromosome))
        self.bestTimeTable = self.parseTimeTableToTuple(TimeTable(self.bestTimeTableChromosome))


    @rx.event
    async def smoothTimeTable(self):
        self.smoothChromosome()
        self.bestTimeTableString = str(TimeTable(self.bestTimeTableChromosome))
        self.bestTimeTable = self.parseTimeTableToTuple(TimeTable(self.bestTimeTableChromosome))

    def smoothChromosome(self):
        smoothedChromosome = self.bestTimeTableChromosome.copy()
        for i in range(1, len(self.bestTimeTableChromosome) - 1):
            if self.constraints[i] == None:
                smoothedChromosome[i] = round((self.bestTimeTableChromosome[i - 1] + self.bestTimeTableChromosome[i] + self.bestTimeTableChromosome[i + 1]) / 3)
        self.bestTimeTableChromosome = smoothedChromosome
        
    @rx.event
    async def saveTimeTable(self):
        from ..components.infoUpload import InfoUploadState
        state = await self.get_state(InfoUploadState)
        if self.saveTimeTableName == "":
            self.saveTimeTableName = "Rozpis " + str(datetime.now())
        state.insertNewTimeTable((self.saveTimeTableName, self.bestTimeTableString))
        self.saveTimeTableName = ""
    
    def setPopulationSize(self, value: str):
        if value == "":
            return
        self.populationSize = int(value)
        self.sliderMax = self.populationSize - 1

def optimizeLine() -> rx.Component:
    return rx.vstack(
        rx.hstack(
            numberImput("Veľkosť populácie", "Veľkosť populácie", OptimizeLineState.populationSize, OptimizeLineState.setPopulationSize, "1", None, OptimizeLineState.populationSize < 1, OptimizeLineState.optimizationRunning),
            numberImput("Počet generácií", "Počet generácií", OptimizeLineState.numberOfGenerations, OptimizeLineState.set_numberOfGenerations, "1", None, OptimizeLineState.numberOfGenerations < 1, OptimizeLineState.optimizationRunning),
            numberImput("Pravdepodobnosť mutácie", "Pravdepodobnosť mutácie", OptimizeLineState.mutationRate, OptimizeLineState.set_mutationRate, "0", "1", (OptimizeLineState.mutationRate < 0) | (OptimizeLineState.mutationRate > 1), OptimizeLineState.optimizationRunning),
            numberImput("Maximálny počet spojov za hodinu", "Maximálny počet spojov za hodinu", OptimizeLineState.maxConnectionsPerHour, OptimizeLineState.set_maxConnectionsPerHour, "1", None, OptimizeLineState.maxConnectionsPerHour < 1, OptimizeLineState.optimizationRunning),
            width="100%",
            spacing="5",
            align="stretch",
        ),
        rx.hstack(
            numberImput("Kapacita vozidla", "Kapacita vozidla", OptimizeLineState.vehicleCapacity, OptimizeLineState.set_vehicleCapacity, "1", None, OptimizeLineState.vehicleCapacity < 1, OptimizeLineState.optimizationRunning),
            numberImput("Miest na sedenie", "Miest na sedenie", OptimizeLineState.vehicleSeats, OptimizeLineState.set_vehicleSeats, "0", None, OptimizeLineState.vehicleSeats < 0, OptimizeLineState.optimizationRunning),
            numberImput("Celkové náklady (Kč/100 miesto-km)", "Kč/100 miesto-km", OptimizeLineState.costPerSeatKm, OptimizeLineState.set_costPerSeatKm, "0", None, OptimizeLineState.costPerSeatKm < 0, OptimizeLineState.optimizationRunning),
            numberImput("Dĺžka trasy", "Dĺžka trasy", OptimizeLineState.routeLength, OptimizeLineState.set_routeLength, "0", None, OptimizeLineState.routeLength < 0, OptimizeLineState.optimizationRunning),
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
                        rx.heading("Generácia " + OptimizeLineState.generationNumber, size="4"),
                        rx.recharts.scatter_chart(
                            rx.recharts.scatter(data=OptimizeLineState.generation),
                            rx.recharts.scatter(data=[OptimizeLineState.selectedScatterPoint], fill="orange", ),
                            rx.recharts.x_axis(data_key="cost", type_="number"),
                            rx.recharts.y_axis(data_key="satisfaction", type_="number"),
                            rx.recharts.legend(),
                            rx.recharts.graphing_tooltip(),
                            width="100%",
                            height=300,
                        ),
                        align_items="center",
                    ),
                    size="3",
                    width="100%",
                ),
                rx.slider(
                    min_=1,
                    max=OptimizeLineState.sliderMax,
                    on_change=OptimizeLineState.setTimeTable.throttle(100),
                    width="100%",
                ),
                rx.cond(
                    OptimizeLineState.bestTimeTable,
                    rx.vstack(   
                        timeTable(OptimizeLineState.bestTimeTable, "Najlepší rozpis"),
                        rx.button(
                            rx.heading("Vyhladiť", size="3"),
                            on_click=[
                                OptimizeLineState.smoothTimeTable(),
                                rx.toast.success("Rozpis bol vyhladený"),
                            ],
                            disabled=rx.cond(
                                OptimizeLineState.optimizationRunning,
                                True,
                                False,
                            ),
                            size="3",
                            width="100%",
                        ),
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
                    rx.text(""),
                ),      
                width="100%",
                spacing="5",
                align="center",
            ),
        ),
        spacing="5",
        width="100%",
        align="center",
    ),