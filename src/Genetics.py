from RandomNumberGenerator import RandomNumberGenerator
from Simulation import Simulation
from models import TimeTable


class Genetics:
    # INIT
    def __init__(self, populationSize, mutationRate, elitismCount, busStops):
        self.populationSize = populationSize
        self.mutationRate = mutationRate
        self.elitismCount = elitismCount
        self.busStops = busStops
        self.generation = []
        self.initPopulation()

    # METHODS
    def initPopulation(self):
        for i in range(self.populationSize):
            self.generation.append(Individual(self.busStops))

        for individual in self.generation:
            individual.calculateFitness()
        self.generation.sort(key=lambda x: x.fitness)

    def crossover(self, parent1, parent2):
        index = RandomNumberGenerator.integers(0, 24)
        newChromosome = parent1.chromosome[:index] + parent2.chromosome[index:]
        return Individual(parent1.busStops, newChromosome)
    
    def parentSelection(self):
        parent1 = self.generation[RandomNumberGenerator.integers(0, self.populationSize)]
        parent2 = self.generation[RandomNumberGenerator.integers(0, self.populationSize)]
        if parent1.fitness < parent2.fitness:
            return parent1
        return parent2
        
    def updateGeneration(self):
        newGeneration = []

        for i in range(self.elitismCount):
            newGeneration.append(self.generation[i])

        for i in range(self.populationSize - self.elitismCount):
            parent1 = self.parentSelection()
            parent2 = self.parentSelection()
            newGeneration.append(self.crossover(parent1, parent2))

        for individual in newGeneration:
            if RandomNumberGenerator.uniform() < self.mutationRate:
                individual.mutate()

        self.generation = newGeneration

        for individual in self.generation:
            individual.calculateFitness()
        self.generation.sort(key=lambda x: x.fitness)

    # STR
    def __str__(self):
        output = ""
        for individual in self.generation:
            output += f"{individual}\n"
        return output

    
class Individual:
    # INIT
    def __init__(self, busStops, chromosome=None):
        self.busStops = busStops
        if chromosome is None:
            self.chromosome = self.generateRandomChromosome()
        else:
            self.chromosome = chromosome
        self.fitness = 0

    # METHODS
    def generateRandomChromosome(self):
        chromosome = [0] * 24
        for i in range(24):
            chromosome[i] = RandomNumberGenerator.integers(0, 30)
        return chromosome

    def calculateFitness(self):
        timeTable = TimeTable(self.chromosome)
        stats = Simulation.run(0, 24*60, self.busStops, timeTable)

        passengersWaitingForNextBusInPercent = stats.busStopStatistics.totalPassengersWaitingForNextBus / stats.busStopStatistics.totalPassengersArrived    # should be minimized
        averagePassengerWaitingTime = stats.busStopStatistics.totalTimeSpentWaiting / stats.busStopStatistics.totalPassengersArrived                        # should be minimized
        passangersLeftUnboardedInPercent = stats.busStopStatistics.totalPassangersLeftUnboarded / stats.busStopStatistics.totalPassengersArrived            # should be minimized
        totalNumberOfBuses = stats.totalNumberOfBuses                                                                                                       # should be minimized                                                      
        averageLoadDeviation = stats.busStatistics.averageLoadInPercent                                                                                     # should be minimized
        if (averageLoadDeviation < 0.7):
            averageLoadDeviation = 1 - averageLoadDeviation / 0.7;
        else:
            averageLoadDeviation = (averageLoadDeviation - 0.7) / 0.3;
        
        self.fitness = passengersWaitingForNextBusInPercent + averagePassengerWaitingTime + passangersLeftUnboardedInPercent + totalNumberOfBuses + averageLoadDeviation

    def mutate(self):
        index = RandomNumberGenerator.integers(0, 24)
        self.chromosome[index] = RandomNumberGenerator.integers(0, 30)

    # STR
    def __str__(self):
        return f"{self.chromosome}: {self.fitness}"