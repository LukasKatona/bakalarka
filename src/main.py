import sys
from InputParser import parseBusStopsFromFile, parseTimeTableFromFile
from EventCalendar import EventCalendar, Event
from SimulationTime import SimulationTime
from Statistics import Statistics
from models import Bus, BusStop

# constants
T_START = 0
T_END = 24*60

# initialize variables
SimulationTime(T_START, T_END)
eventCalendar = EventCalendar()
buses = []

# parse bus stops input file
busStopsFile = open(sys.argv[1], "r")
busStops = parseBusStopsFromFile(busStopsFile)
busStopsFile.close()

# parse time table input file
timeTableFile = open(sys.argv[2], "r")
timeTable = parseTimeTableFromFile(timeTableFile)
timeTableFile.close()

# populate event calendar with bus arrival events
for time in timeTable.getAllTimes():
    # create bus
    bus = Bus(busStops[0], 80)
    buses.append(bus)

    # add bus arrival events
    for busStop in busStops:
        eventCalendar.addEvent(Event(time + busStop.timeDeltaToArrive, bus.runBusStopSequence, busStop))


# print events to file
eventsFile = open(sys.argv[3], "w")
eventsFile.write(str(eventCalendar))
eventsFile.close()

# main simulation loop
while eventCalendar.isEmpty() == False:
    # get next event
    event = eventCalendar.getNextEvent()

    # check if event is beyond simulation time
    if (event.time > T_END):
        break

    # advance time
    SimulationTime.forward(event.time)

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


Statistics(len(buses), busStopStats, busStats)
Statistics.print()
Statistics.busStopStatistics.plotTimeSpentWaitingPerHour()
