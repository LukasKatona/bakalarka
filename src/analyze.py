import sys
from InputParser import InputParser
from Simulation import Simulation

busStops = InputParser.parseBusStopsFromFile(sys.argv[1])
timeTable = InputParser.parseTimeTableFromFile(sys.argv[2])
stats = Simulation.run(0, 24*60, busStops, timeTable)
stats.saveAllGraphs()
stats.print()