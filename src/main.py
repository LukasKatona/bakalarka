import sys
from InputParser import InputParser
from EventCalendar import EventCalendar, Event
from Simulation import Simulation
from Statistics import Statistics
from models import Bus, BusStop

# initialize variables
# parse bus stops input file
busStops = InputParser.parseBusStopsFromFile(sys.argv[1])
# parse time table input file
timeTable = InputParser.parseTimeTableFromFile(sys.argv[2])
Simulation.run(0, 24*60, busStops, timeTable)


