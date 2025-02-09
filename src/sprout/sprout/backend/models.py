from enum import Enum
from .RandomNumberGenerator import RandomNumberGenerator
from .Simulation import Simulation
from .Statistics import BusStatistics, BusStopStatistics

# ------------------------------ BUSSTOP ------------------------------
class BusStop:

    # STATES
    class State(Enum):
        Idle = 1
        BusArrived = 2
        BusBoarding = 3

    # INPUT SIGNALS
    class InputSignals(Enum):
        BusArrived = 1
        StartBoarding = 2
        FinishBoarding = 3

    def triggerInputSignal(self, signal):
        if signal == BusStop.InputSignals.BusArrived:
            self.busArrived()
        elif signal == BusStop.InputSignals.StartBoarding:
            self.startBoarding()
        elif signal == BusStop.InputSignals.FinishBoarding:
            self.finishBoarding()

    # OUTPUT SIGNALS
    def setOutputSignals(self):
        pass

    def triggerOutputSignal(self, signal):
        pass

    # INIT
    def __init__(self, name, timeDeltaToArrive, passengerArrivalRatesPerHour, leavingPassengersRate):
        self.name = name
        self.timeDeltaToArrive = timeDeltaToArrive
        self.passengerArrivalRatesPerHour = passengerArrivalRatesPerHour
        self.leavingPassengersRate = leavingPassengersRate
        self.state = BusStop.State.Idle
        self.timeOfLastBusArrival = Simulation.startTime
        self.timeIntervalBetweenBuses = 0
        self.waitingPassangersArrivalTimes = []
        self.setOutputSignals()
        self.stats = BusStopStatistics(name)
    
    def clear(self):
        self.timeOfLastBusArrival = Simulation.startTime
        self.timeIntervalBetweenBuses = 0
        self.waitingPassangersArrivalTimes = []
        self.stats.clear()

    # METHODS
    def busArrived(self):
        self.state = BusStop.State.BusArrived
        self.timeIntervalBetweenBuses = Simulation.currentTime - self.timeOfLastBusArrival

    def startBoarding(self):
        self.state = BusStop.State.BusBoarding
        self.waitingPassangersArrivalTimes += self.generatePassengers()
        self.waitingPassangersArrivalTimes.sort()

        
    def finishBoarding(self):
        self.state = BusStop.State.Idle
        self.timeOfLastBusArrival = Simulation.currentTime

    def generatePassengers(self):
        # find the rate for the current hour
        lambdaValue = 0
        currentHour = Simulation.getHour()
        for hourRate in self.passengerArrivalRatesPerHour:
            if hourRate.hour == currentHour:
                lambdaValue = hourRate.rate / 60
                break

        # if there is no rate for the current hour, no passengers will arrive
        if lambdaValue == 0:
            return []
        
        # restrict the waiting time for the first bus to 15 minutes
        if self.timeOfLastBusArrival == Simulation.startTime:
            self.timeOfLastBusArrival = Simulation.currentTime - 15

        # generate passengers
        arrivalTimes = []
        currentTime = self.timeOfLastBusArrival
        while currentTime < Simulation.currentTime:
            interArrivalTime = RandomNumberGenerator.exponential(1 / lambdaValue)
            currentTime += interArrivalTime

            if currentTime < Simulation.currentTime:
                arrivalTimes.append(currentTime)
                # update statistics
                self.stats.updatePassengersArrivedPerHour(1, currentTime // 60 % 24)

        return arrivalTimes

    # STR
    def __str__(self):
        return f"{self.name}: {self.timeDeltaToArrive}"
    
    def printAllInfo(self):
        print(f"{self.name}: {self.timeDeltaToArrive}, {self.passengerArrivalRatesPerHour}, {self.leavingPassengersRate}")


# ----------------------------- TIMETABLE -----------------------------
class TimeTable:
    # INIT
    def __init__(self, chromosome=None):
        self.rows = []
        if chromosome is not None:
            self.generateFromChromosome(chromosome)

    class TimeTableRow:
        # INIT
        def __init__(self, hour, minutes):
            self.hour = hour
            self.minutes = minutes
        
    # METHODS
    def addRow(self, hour, minutes):
        self.rows.append(TimeTable.TimeTableRow(hour, minutes))

    def getAllTimes(self):
        times = []
        for row in self.rows:
            for minute in row.minutes:
                times.append(row.hour * 60 + minute)
        return times
    
    def getChromosome(self):
        chromosome = [0] * 24
        for row in self.rows:
            chromosome[row.hour] = len(row.minutes)
        return chromosome
    
    def generateFromChromosome(self, chromosome):
        for i in range(len(chromosome)):
            if chromosome[i] != "0":
                # generate array of minutes equally distributed in one hour based on number in parts[i]
                minutes = [int((j + 1) * 60 / (int(chromosome[i]) + 1)) for j in range(int(chromosome[i]))]
                self.addRow(i, minutes)


    def __str__(self):
        return "\n".join([f"{row.hour:02}: " + ", ".join([f"{minute:02}" for minute in row.minutes]) for row in self.rows])


# -------------------------------- BUS --------------------------------
class Bus:
    busCounter = 1

    # STATES
    class State(Enum):
        Traveling = 1
        Arrived = 2
        Boarding = 3

    # INPUT SIGNALS
    def triggerInputSignal(self, signal):
        pass

    # OUTPUT SIGNALS
    class OutputSignals(Enum):
        Arrival = 1
        Boarding = 2
        Departure = 3

    def setOutputSignals(self):
        self.signals =  {
            Bus.OutputSignals.Arrival: [(self.currentBusStop, BusStop.InputSignals.BusArrived)],
            Bus.OutputSignals.Boarding: [(self.currentBusStop, BusStop.InputSignals.StartBoarding)],
            Bus.OutputSignals.Departure: [(self.currentBusStop, BusStop.InputSignals.FinishBoarding)]
        }

    def triggerOutputSignal(self, signal):
        for inputSignal in self.signals[signal]:
            inputSignal[0].triggerInputSignal(inputSignal[1])

    # INIT
    def __init__(self, firstBusStop, capacity):
        self.busNumber = Bus.busCounter
        Bus.busCounter += 1
        self.state = Bus.State.Traveling
        self.currentBusStop = firstBusStop
        self.capacity = capacity
        self.load = 0
        self.setOutputSignals()
        self.stats = BusStatistics(self.busNumber, capacity)

    # STATE MACHINE
    def runBusStopSequence(self, busStop):
        self.currentBusStop = busStop
        self.setOutputSignals()
        self.arriveAtStop()
        self.boardPassengers()
        self.departFromStop()

    # METHODS
    def arriveAtStop(self):
        self.state = Bus.State.Arrived
        # notify bus stop that new bus has arrived
        self.triggerOutputSignal(Bus.OutputSignals.Arrival)
        # number of passengers leaving the bus
        numberOfLeavingPassengers = round(self.load * self.currentBusStop.leavingPassengersRate)
        self.load = max(0, self.load - numberOfLeavingPassengers)
        # update statistics
        self.currentBusStop.stats.updatePassengersDepartedPerHour(numberOfLeavingPassengers, Simulation.getHour())
        
    def boardPassengers(self):
        self.state = Bus.State.Boarding
        # notify bus stop to generate new passengers
        self.triggerOutputSignal(Bus.OutputSignals.Boarding)
        # board passengers, if there is capacity and there are passengers waiting
        while self.load < self.capacity and len(self.currentBusStop.waitingPassangersArrivalTimes) > 0 and self.currentBusStop.waitingPassangersArrivalTimes[0] <= Simulation.currentTime:
            self.load += 1
            passengerArrivalTime = self.currentBusStop.waitingPassangersArrivalTimes.pop(0)
            # update statistics
            self.currentBusStop.stats.updateTimeSpentWaitingPerHour(Simulation.currentTime - passengerArrivalTime, Simulation.getHour())
            self.stats.updateTotalPassengersTransported(1)
        # update statistics
        self.currentBusStop.stats.updatePassengersWaitingForNextBusPerHour(len(self.currentBusStop.waitingPassangersArrivalTimes), Simulation.getHour())
        self.stats.updateLoadPerBusStop(self.load, self.currentBusStop.name)
        
    def departFromStop(self):
        self.state = Bus.State.Traveling
        # notify bus stop that bus has departed
        self.triggerOutputSignal(Bus.OutputSignals.Departure)    

    # STR
    def __str__(self):
        return f"Bus #{self.busNumber}: {self.currentBusStop.name}, {self.state}, {self.load}/{self.capacity}"