import sys
from Genetics import Genetics
from InputParser import InputParser
from models import TimeTable

busStops = InputParser.parseBusStopsFromFile(sys.argv[1])
# timeTable = InputParser.parseTimeTableFromFile(sys.argv[2])
# Simulation.run(0, 24*60, busStops, timeTable)

genetics = Genetics(20, 0.01, 0.9, 2, busStops)


for i in range(500):
    print(str(i) + " generation\n")
    genetics.updateGeneration()

timeTable = TimeTable(genetics.generation[0].chromosome)
print(timeTable)

