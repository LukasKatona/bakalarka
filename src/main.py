import sys
from Genetics import Genetics
from InputParser import InputParser
from models import TimeTable

busStops = InputParser.parseBusStopsFromFile(sys.argv[1])
# timeTable = InputParser.parseTimeTableFromFile(sys.argv[2])
# Simulation.run(0, 24*60, busStops, timeTable)

genetics = Genetics(20, 1.0, 0, busStops)

last3Chromosomes = []
for i in range(500):
    print(str(i) + " generation: best fitness: " + str(genetics.generation[0].fitness))
    timeTable = TimeTable(genetics.generation[0].chromosome)
    print(timeTable)
    genetics.updateGeneration()
    last3Chromosomes.append(genetics.generation[0].chromosome)
    if len(last3Chromosomes) == 3:
        if last3Chromosomes[0] == last3Chromosomes[1] == last3Chromosomes[2]:
            break
        last3Chromosomes.pop(0)


    
