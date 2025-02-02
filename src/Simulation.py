from datetime import timedelta
import sys

from EventCalendar import Event, EventCalendar
from Statistics import Statistics

class Simulation:
    # Static global variables
    startTime = 0
    currentTime = 0
    endTime = 0

    # INIT
    def __init__(self, initialTime, endTime):
        Simulation.startTime = initialTime
        Simulation.currentTime = initialTime
        Simulation.endTime = endTime

    # METHODS
    @staticmethod
    def printCurrentTime():
        print(f"{(Simulation.startTime + timedelta(minutes=Simulation.currentTime)).time().strftime('%H:%M')}")

    @staticmethod
    def printCurrentTimeAndMessage(message):
        print(f"{(Simulation.startTime + timedelta(minutes=Simulation.currentTime)).time().strftime('%H:%M')}: {message}")

    @staticmethod
    def forward(eventTime):
        Simulation.currentTime = eventTime

    @staticmethod
    def getHour():
        return Simulation.currentTime // 60 % 24
    
    @staticmethod
    def run(startTime, endTime, busStops, timeTable):
        from models import Bus, BusStop

        # initialize variables
        Simulation(startTime, endTime)
        eventCalendar = EventCalendar()
        buses = []

        # populate event calendar with bus arrival events
        for time in timeTable.getAllTimes():
            # create bus
            bus = Bus(busStops[0], 80)
            buses.append(bus)

            # add bus arrival events
            for busStop in busStops:
                eventCalendar.addEvent(Event(time + busStop.timeDeltaToArrive, bus.runBusStopSequence, busStop))

        # main simulation loop
        while eventCalendar.isEmpty() == False:
            # get next event
            event = eventCalendar.getNextEvent()

            # check if event is beyond simulation time
            if (event.time > Simulation.endTime):
                break

            # advance time
            Simulation.forward(event.time)

            # execute event
            event()

        # update statistics
        busStopStats = []
        for busStop in busStops:
            if isinstance(busStop, BusStop):
                busStop.stats.updateTotalPassangersLeftUnboarded(len(busStop.waitingPassangersArrivalTimes))
                busStop.stats.agregateTotal()
                busStopStats.append(busStop.stats)

        busStats = []
        for bus in buses:
            if isinstance(bus, Bus):
                bus.stats.agregateTotal()
                busStats.append(bus.stats)

        return Statistics(len(buses), busStopStats, busStats, "sk")
