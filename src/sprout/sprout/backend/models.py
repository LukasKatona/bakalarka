"""
This file contains the Bus, BusStop, and TimeTable classes, which are used in the simulation of a bus system.
"""

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

    def triggerInputSignal(self, signal: InputSignals):
        """
        Trigger the input signal for the bus stop. This will change the state of the bus stop and update the statistics.

        :param signal: The input signal to be triggered.
        :type signal: InputSignals
        """
        if signal == BusStop.InputSignals.BusArrived:
            self.busArrived()
        elif signal == BusStop.InputSignals.StartBoarding:
            self.startBoarding()
        elif signal == BusStop.InputSignals.FinishBoarding:
            self.finishBoarding()

    # OUTPUT SIGNALS
    def setOutputSignals(self):
        """
        Bus stop has no output signals. This method is a placeholder for future use.
        """
        pass

    def triggerOutputSignal(self, signal):
        """
        Bus stop has no output signals. This method is a placeholder for future use.

        :param signal: The output signal to be triggered.
        :type signal: OutputSignals
        """
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
        self.waitingPassengersArrivalTimes = []
        self.setOutputSignals()
        self.stats = BusStopStatistics(name)
    
    # METHODS
    def clear(self):
        """
        Clear the bus stop statistics and reset the state of the bus stop.
        """
        self.timeOfLastBusArrival = Simulation.startTime
        self.timeIntervalBetweenBuses = 0
        self.waitingPassengersArrivalTimes = []
        self.stats.clear()

    def busArrived(self):
        """
        Update the state of the bus stop when a bus arrives. This will set the state to BusArrived and update the time it took for the next bus to arrive.
        """
        self.state = BusStop.State.BusArrived
        self.timeIntervalBetweenBuses = Simulation.currentTime - self.timeOfLastBusArrival

    def startBoarding(self):
        """
        Update the state of the bus stop when boarding starts. This will set the state to BusBoarding and generate new passengers.
        """
        self.state = BusStop.State.BusBoarding
        self.waitingPassengersArrivalTimes += self.generatePassengers()
        self.waitingPassengersArrivalTimes.sort()

        
    def finishBoarding(self):
        """
        Update the state of the bus stop when boarding finishes. This will set the state to Idle and update the time of the last bus arrival.
        """
        self.state = BusStop.State.Idle
        self.timeOfLastBusArrival = Simulation.currentTime
        self.waitingPassengersArrivalTimes = []

    def generatePassengers(self):
        """
        Generate passengers based on the passenger arrival rates per hour. This will generate a list of arrival times for the passengers.
        The arrival times are generated using an exponential distribution based on the rate for the current hour.
        Instead of using poisson distribution for generating the number of passengers,
        we use an exponential distribution to generate the time between passenger arrivals.
        Generated time is added to the time of the last bus arrival to get the arrival time of the passenger.
        Local simulation time is forwarded by the generated time.
        This proccess is repeated until the current simulation time is reached.

        :return: A list of arrival times for the passengers.
        :rtype: list[float]
        """
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
    def addRow(self, hour: int, minutes: list[int]):
        """
        Add a row to the time table. The row contains the hour and a list of minutes.

        :param hour: The hour of the row.
        :type hour: int
        :param minutes: The list of minutes for the row.
        :type minutes: list[int]
        """
        self.rows.append(TimeTable.TimeTableRow(hour, minutes))

    def getAllTimes(self) -> list[int]:
        """
        Get all times in the time table. The times are represented as a list of integers, where each integer is the time in minutes since midnight.

        :return: The list of departure times in minutes since midnight.
        :rtype: list[int]
        """
        times = []
        for row in self.rows:
            for minute in row.minutes:
                times.append(row.hour * 60 + minute)
        return times
    
    def getChromosome(self) -> list[int]:
        """
        Get the chromosome representation of the time table. The chromosome is a list of integers, where each integer represents the number of departures in the corresponding hour.

        :return: The chromosome representation of the time table.
        :rtype: list[int]
        """
        chromosome = [0] * 24
        for row in self.rows:
            chromosome[row.hour] = len(row.minutes)
        return chromosome
    
    def generateFromChromosome(self, chromosome: list[int]):
        """
        Generate the time table from a chromosome. The chromosome is a list of integers, where each integer represents the number of departures in the corresponding hour.
        The minites for each hour are generated based on the number of departures, which are evenly distributed over the hour.

        :param chromosome: The chromosome representation of the time table.
        :type chromosome: list[int]
        """
        for i in range(len(chromosome)):
            if chromosome[i] != "0":
                minutes = [int((j) * 60 / (int(chromosome[i]))) for j in range(int(chromosome[i]))]
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
        """
        Bus has no input signals. This method is a placeholder for future use.

        :param signal: The input signal to be triggered.
        :type signal: InputSignals
        """
        pass

    # OUTPUT SIGNALS
    class OutputSignals(Enum):
        Arrival = 1
        Boarding = 2
        Departure = 3
        
    def setOutputSignals(self):
        """
        Binds the output signals of the bus to the input signals of the bus stop.
        The output signals are used to notify the bus stop when a bus has arrived, started boarding, or departed.
        The bus output signals could be binded to multiple other models.
        For every output signal, a list of tuples is created, where each tuple contains the model that will receive the signal and the input signal that will be triggered.
        """
        self.signals =  {
            Bus.OutputSignals.Arrival: [(self.currentBusStop, BusStop.InputSignals.BusArrived)],
            Bus.OutputSignals.Boarding: [(self.currentBusStop, BusStop.InputSignals.StartBoarding)],
            Bus.OutputSignals.Departure: [(self.currentBusStop, BusStop.InputSignals.FinishBoarding)]
        }

    def triggerOutputSignal(self, signal: OutputSignals):
        """
        Trigger the output signal for the bus. This will trigger all input signals that are bound to the output signal.

        :param signal: The output signal to be triggered.
        :type signal: OutputSignals
        """
        for inputSignal in self.signals[signal]:
            inputSignal[0].triggerInputSignal(inputSignal[1])

    # INIT
    def __init__(self, firstBusStop, capacity, seats):
        self.busNumber = Bus.busCounter
        Bus.busCounter += 1
        self.state = Bus.State.Traveling
        self.currentBusStop = firstBusStop
        self.capacity = capacity
        self.seats = seats
        self.load = 0
        self.setOutputSignals()
        self.stats = BusStatistics(self.busNumber, capacity, seats)

    # STATE MACHINE
    def runBusStopSequence(self, busStop: BusStop):
        """
        Run the bus stop sequence. This will set the current bus stop, bind the output signals to the input signals of the bus stop, and trigger the output signals.
        The bus will arrive at the stop, board passengers, and depart from the stop.

        :param busStop: The bus stop on which the bus will stop.
        :type busStop: BusStop
        """
        self.currentBusStop = busStop
        self.setOutputSignals()
        self.arriveAtStop()
        self.boardPassengers()
        self.departFromStop()

    # METHODS
    def arriveAtStop(self):
        """
        Update the state of the bus when it arrives at a stop. This will set the state to Arrived and update the statistics.
        The bus will notify the bus stop that it has arrived, and the number of passengers leaving the bus will be calculated based on the leaving passengers rate.
        """
        self.state = Bus.State.Arrived
        # notify bus stop that new bus has arrived
        self.triggerOutputSignal(Bus.OutputSignals.Arrival)
        # number of passengers leaving the bus
        numberOfLeavingPassengers = round(self.load * self.currentBusStop.leavingPassengersRate)
        self.load = max(0, self.load - numberOfLeavingPassengers)
        # update statistics
        self.currentBusStop.stats.updatePassengersDepartedPerHour(numberOfLeavingPassengers, Simulation.getHour())
        
    def boardPassengers(self):
        """
        Update the state of the bus when boarding starts. This will set the state to Boarding and update the statistics.
        The bus will notify the bus stop that boarding has started, and the number of passengers boarding the bus will be calculated based on the number of waiting passengers and the bus capacity.
        The bus will board passengers until it is full or there are no more waiting passengers.
        """
        self.state = Bus.State.Boarding
        # notify bus stop to generate new passengers
        self.triggerOutputSignal(Bus.OutputSignals.Boarding)
        # board passengers, if there is capacity and there are passengers waiting
        while len(self.currentBusStop.waitingPassengersArrivalTimes) > 0 and self.currentBusStop.waitingPassengersArrivalTimes[0] <= Simulation.currentTime:
            if self.load == self.capacity:
                break;
            self.updatePassengerSatisfaction()
            self.load += 1
            passengerArrivalTime = self.currentBusStop.waitingPassengersArrivalTimes.pop(0)
            # update statistics
            self.currentBusStop.stats.updateTimeSpentWaitingPerHour(Simulation.currentTime - passengerArrivalTime, Simulation.getHour())
            self.stats.updateTotalPassengersTransported(1)
        # update statistics
        self.currentBusStop.stats.updatePassengersLeftUnboardedPerHour(len(self.currentBusStop.waitingPassengersArrivalTimes), Simulation.getHour())
        for i in range(len(self.currentBusStop.waitingPassengersArrivalTimes)):
            self.stats.updatePassengerSatisfactions(0)
        self.stats.updateLoadPerBusStop(self.load, self.currentBusStop.name)
        
    def departFromStop(self):
        """
        Update the state of the bus when it departs from a stop. This will set the state to Traveling and update the statistics.
        The bus will notify the bus stop that it has departed.
        """
        self.state = Bus.State.Traveling
        # notify bus stop that bus has departed
        self.triggerOutputSignal(Bus.OutputSignals.Departure)    

    def updatePassengerSatisfaction(self):
        """
        Update the passenger satisfaction based on the current load of the bus and the number of seats.
        """
        if self.load <= self.seats:
            satisfaction = 1
        elif self.load > self.seats:
            satisfaction = 1 - (self.load - self.seats)/(self.capacity - self.seats)
        self.stats.updatePassengerSatisfactions(satisfaction)

    # STR
    def __str__(self):
        return f"Bus #{self.busNumber}: {self.currentBusStop.name}, {self.state}, {self.load}/{self.capacity}"
