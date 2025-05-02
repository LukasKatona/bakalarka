"""
This file contains the Simulation class, which is used to simulate the bus system.
"""

from datetime import timedelta

from .EventCalendar import Event, EventCalendar
from .Statistics import Statistics, averageStatistics

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
    def forward(eventTime: int):
        """
        Move the simulation time forward to the event time.

        :param eventTime: The time of the event to move to.
        :type eventTime: int
        """
        Simulation.currentTime = eventTime

    @staticmethod
    def getHour() -> int:
        """
        Get the current hour of the simulation.

        :return: The current hour of the simulation.
        :rtype: int
        """
        return Simulation.currentTime // 60 % 24
    
    @staticmethod
    def run(startTime: int, endTime: int, busStops, timeTable, vehicleCapacity: int, vehicleSeats: int) -> Statistics:
        """
        Run the simulation for a given time period and return the statistics.

        :param startTime: The start time of the simulation.
        :type startTime: int
        :param endTime: The end time of the simulation.
        :type endTime: int
        :param busStops: The list of bus stops to be used in the simulation.
        :type busStops: list[BusStop]
        :param timeTable: The timetable to be used in the simulation.
        :type timeTable: TimeTable
        :param vehicleCapacity: The capacity of the vehicle.
        :type vehicleCapacity: int
        :param vehicleSeats: The number of seats in the vehicle.
        :type vehicleSeats: int
        :return: The statistics of the simulation.
        :rtype: Statistics
        """
        from .models import Bus, BusStop

        for busStop in busStops:
            busStop.clear()

        # initialize variables
        Simulation.startTime = startTime
        Simulation.currentTime = startTime
        Simulation.endTime = endTime
        eventCalendar = EventCalendar()
        buses = []

        # populate event calendar with bus arrival events
        for time in timeTable.getAllTimes():
            # create bus
            bus = Bus(busStops[0], vehicleCapacity, vehicleSeats)
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
                busStop.stats.agregateTotal()
                busStopStats.append(busStop.stats)

        busStats = []
        for bus in buses:
            if isinstance(bus, Bus):
                bus.stats.agregateTotal()
                busStats.append(bus.stats)

        return Statistics(len(buses), busStopStats, busStats, "sk")
    
    @staticmethod
    def runMultipleThanAverage(startTime: int, endTime: int, busStops, timeTable, vehicleCapacity: int, vehicleSeats: int, numberOfSimulations: int) -> Statistics:
        """
        Run multiple simulations and return the average statistics.

        :param startTime: The start time of the simulation.
        :type startTime: int
        :param endTime: The end time of the simulation.
        :type endTime: int
        :param busStops: The list of bus stops to be used in the simulation.
        :type busStops: list[BusStop]
        :param timeTable: The timetable to be used in the simulation.
        :type timeTable: TimeTable
        :param vehicleCapacity: The capacity of the vehicle.
        :type vehicleCapacity: int
        :param vehicleSeats: The number of seats in the vehicle.
        :type vehicleSeats: int
        :param numberOfSimulations: The number of simulations to run.
        :type numberOfSimulations: int
        :return: The statistics of the simulation.
        :rtype: Statistics
        """
        statsList = []
        for i in range(numberOfSimulations):
            stats = Simulation.run(startTime, endTime, busStops, timeTable, vehicleCapacity, vehicleSeats)
            statsList.append(stats)
        return averageStatistics(statsList)