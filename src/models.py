from enum import Enum

# ------------------------------ BUSSTOP ------------------------------
class BusStop:

    # STATES
    class State(Enum):
        Idle = 1
        BusArrived = 2
        Boarding = 3

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
    def initOutputSignals(self):
        pass

    def triggerOutputSignal(self, signal):
        pass

    # INIT
    def __init__(self, name, timeDeltaToArrive):
        self.name = name
        self.timeDeltaToArrive = timeDeltaToArrive
        self.state = BusStop.State.Idle
        self.initOutputSignals()

    # METHODS
    def busArrived(self):
        self.state = BusStop.State.BusArrived

    def startBoarding(self):
        self.state = BusStop.State.Boarding
        
    def finishBoarding(self):
        self.state = BusStop.State.Idle

    # STR
    def __str__(self):
        return f"{self.name}: {self.timeDeltaToArrive}"


# ----------------------------- TIMETABLE -----------------------------
class TimeTable:
    # INIT
    def __init__(self):
        self.rows = []

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

    def __str__(self):
        return "\n".join([f"{row.hour:02}: " + ", ".join([f"{minute:02}" for minute in row.minutes]) for row in self.rows])


# -------------------------------- BUS --------------------------------
class Bus:
    # STATES
    class State(Enum):
        Starting = 1
        Traveling = 2
        Arrived = 3
        Boarding = 4
        Departed = 5
        Finished = 6

    # INPUT SIGNALS
    def triggerInputSignal(self, signal):
        pass

    # OUTPUT SIGNALS
    class OutputSignals(Enum):
        Arrival = 1
        Boarding = 2
        Departure = 3

    def initOutputSignals(self):
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
        self.state = Bus.State.Starting
        self.currentBusStop = firstBusStop
        self.capacity = capacity
        self.load = 0
        self.initOutputSignals()

    # STATE MACHINE
    def runBusStopSequence(self, busStop):

        self.state = Bus.State.Traveling
        self.currentBusStop = busStop

        while self.state != Bus.State.Departed:
            if self.state == Bus.State.Traveling:
                self.arriveAtStop()
            elif self.state == Bus.State.Arrived:
                self.boardPassengers()
            elif self.state == Bus.State.Boarding:
                self.departFromStop()

    # METHODS
    def arriveAtStop(self):
        self.state = Bus.State.Arrived
        self.triggerOutputSignal(Bus.OutputSignals.Arrival)

        print(self)
        
    def boardPassengers(self):
        self.state = Bus.State.Boarding
        self.triggerOutputSignal(Bus.OutputSignals.Boarding)

        print(self)

    def departFromStop(self):
        self.state = Bus.State.Departed
        self.triggerOutputSignal(Bus.OutputSignals.Departure)    

        print(self)

    # STR
    def __str__(self):
        return f"Bus: {self.currentBusStop.name}, {self.state}, {self.load}/{self.capacity}"