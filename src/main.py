import sys
from InputParser import parseBusStopsFromFile, parseTimeTableFromFile
from EventCalendar import EventCalendar, Event
from Time import forwardModelTime, printCurrentTimeAndMessage

# buss_stops = [
#     BusStop("Stop 1", 10, 1),
#     BusStop("Stop 2", 20, 1),
#     BusStop("Stop 3", 30, 1),
#     BusStop("Stop 4", 20, 1),
#     BusStop("Stop 5", 10, 1)
# ]

# bus_line = BusLine(46, buss_stops, [5, 6, 4, 7])

# bus = Bus(5, bus_line)

# print("Simulation started")

# while bus.state != Bus.State.Finished:
#     if bus.state == Bus.State.Starting:
#         bus.start()
#     if bus.state == Bus.State.Traveling:
#         bus.travel_to_next_stop()
#     elif bus.state == Bus.State.Arrived:
#         bus.arrive_at_stop()
#     elif bus.state == Bus.State.Boarding:
#         bus.board_passengers()
#     elif bus.state == Bus.State.Departed:
#         bus.depart_stop()

# print("Simulation finished")

busStopsFile = open(sys.argv[1], "r")
busStops = parseBusStopsFromFile(busStopsFile)
busStopsFile.close()

timeTableFile = open(sys.argv[2], "r")
timeTable = parseTimeTableFromFile(timeTableFile)
timeTableFile.close()

eventCalendar = EventCalendar(0)

for busStop in busStops:
    for time in timeTable.getAllTimes():
        time = time + busStop.timeDeltaToArrive
        eventCalendar.addEvent(Event(time, busStop))

# print events to file
eventsFile = open(sys.argv[3], "w")
eventsFile.write(str(eventCalendar))
eventsFile.close()

