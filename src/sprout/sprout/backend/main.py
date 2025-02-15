import sys
from .Genetics import Genetics
from .InputParser import InputParser
from .Simulation import Simulation
from .models import TimeTable

busStops = InputParser.parseBusStopsFromFile(sys.argv[1])
timeTable = InputParser.parseTimeTableFromFile(sys.argv[2])
#Simulation.run(0, 24*60, busStops, timeTable)

constraints = [0,0,0,0,0,'x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x',0]
#constraints = ['x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x']
genetics = Genetics(10, 0.3, 2, busStops, constraints)

lastChromosomes = []
for i in range(100):
    print(str(i) + " generation - best score: " + str(genetics.generation[0].totalScore))
    print(genetics)
    genetics.updateGeneration()
    lastChromosomes.append(genetics.generation[0].chromosome)
    if len(lastChromosomes) == 5:
        if lastChromosomes[0] == lastChromosomes[1] == lastChromosomes[2] == lastChromosomes[3] == lastChromosomes[4]:
            break
        lastChromosomes.pop(0)

timeTable = TimeTable(genetics.generation[0].chromosome)
print(timeTable)
stats = Simulation.run(0, 24*60, busStops, timeTable)
stats.saveAllGraphs()


    
