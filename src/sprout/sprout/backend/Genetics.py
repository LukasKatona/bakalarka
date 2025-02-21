import multiprocessing

from .RandomNumberGenerator import RandomNumberGenerator
from .Simulation import Simulation
from .models import TimeTable


class Genetics:
    # INIT
    def __init__(self, populationSize, mutationRate, elitismCount, busStops, constraints, initialChromosome=None,):
        self.populationSize = populationSize
        self.mutationRate = mutationRate
        self.elitismCount = elitismCount
        self.busStops = busStops
        self.constraints = constraints
        self.generation = []
        self.initPopulation(initialChromosome)

    # METHODS
    def initPopulation(self, initialChromosome=None):
        for i in range(self.populationSize):
            self.generation.append(Individual(self.mutationRate, self.busStops, self.constraints))

        if initialChromosome is not None:
            self.generation.pop(0)
            self.generation.append(Individual(self.mutationRate, self.busStops, self.constraints, initialChromosome))

        proccesses = [multiprocessing.Process(target=self._calculate_fitness_wrapper, args=[individual]) for individual in self.generation]
        for process in proccesses:
            process.start()
        for process in proccesses:
            process.join()
            
        self.sortGeneration()

    def crossover(self, parent1, parent2):
        newChromosome1 = [0]*24
        newChromosome2 = [0]*24
        for i in range(24):
            if RandomNumberGenerator.uniform() < 0.5:
                newChromosome1[i] = parent1.chromosome[i]
                newChromosome2[i] = parent2.chromosome[i]
            else:
                newChromosome1[i] = parent2.chromosome[i]
                newChromosome2[i] = parent1.chromosome[i]
        return Individual(self.mutationRate, self.busStops, self.constraints, newChromosome1), Individual(self.mutationRate, self.busStops, self.constraints, newChromosome2)
    
    def parentSelection(self):
        parent1 = self.generation[RandomNumberGenerator.integers(0, self.populationSize)]
        parent2 = self.generation[RandomNumberGenerator.integers(0, self.populationSize)]
        if parent1.totalScore < parent2.totalScore:
            return parent1
        return parent2
        
    def updateGeneration(self):
        newGeneration = []

        for i in range(self.elitismCount):
            newGeneration.append(self.generation[i])

        for i in range(int((self.populationSize - self.elitismCount)/2)):
            parent1 = self.parentSelection()
            parent2 = self.parentSelection()
            child1, child2 = self.crossover(parent1, parent2)
            newGeneration.append(child1)
            newGeneration.append(child2)

        for individual in newGeneration:
            individual.mutate()
                
        self.generation = newGeneration

        proccesses = [multiprocessing.Process(target=self._calculate_fitness_wrapper, args=[individual]) for individual in self.generation]
        for process in proccesses:
            process.start()
        for process in proccesses:
            process.join()

        self.sortGeneration()
    
    def _calculate_fitness_wrapper(individual):
        individual.calculateFitness()

    def sortGeneration(self):
        for individual in self.generation:
            individual.totalScore = individual.totalNumberOfBusesFitness

        self.generation.sort(key=lambda x: x.totalScore)

        

    # STR
    def __str__(self):
        output = ""
        for individual in self.generation:
            output += f"{individual}\n"
        return output

    
class Individual:
    # INIT
    def __init__(self, mutationRate, busStops, constraints, chromosome=None):
        self.mutationRate = mutationRate
        self.busStops = busStops
        self.constraints = constraints
        if chromosome is None:
            self.chromosome = self.generateRandomChromosome()
        else:
            self.chromosome = chromosome
        self.passengerWaitingTimeFitness = 0
        self.passengerWaitingForNextBusFitness = 0
        self.passengersLeftUnboardedFitness = 0
        self.totalNumberOfBusesFitness = 0
        self.averageLoadDeviationFitness = 0
        self.totalScore = 0
        self.fitness = 0

    # METHODS
    def generateRandomChromosome(self):
        chromosome = [0] * 24
        for i in range(24):
            if self.constraints[i] != 'x':
                chromosome[i] = self.constraints[i]
            else:
                chromosome[i] = RandomNumberGenerator.integers(1, 30)
        return chromosome

    def calculateFitness(self):
        timeTable = TimeTable(self.chromosome)
        stats = Simulation.run(0, 24*60, self.busStops, timeTable)
        self.passengerWaitingForNextBusFitness = stats.busStopStatistics.totalPassengersWaitingForNextBus / stats.busStopStatistics.totalPassengersArrived    # should be minimized
        self.passengerWaitingTimeFitness = stats.busStopStatistics.totalTimeSpentWaiting / stats.busStopStatistics.totalPassengersArrived                        # should be minimized
        self.passengersLeftUnboardedFitness = stats.busStopStatistics.totalPassangersLeftUnboarded / stats.busStopStatistics.totalPassengersArrived            # should be minimized
        self.totalNumberOfBusesFitness = stats.totalNumberOfBuses                                                                                                       # should be minimized                                                      
        self.averageLoadDeviationFitness = stats.busStatistics.averageLoadInPercent                                                                                     # should be minimized
        if (self.averageLoadDeviationFitness < 0.7):
            self.averageLoadDeviationFitness = 1 - self.averageLoadDeviationFitness / 0.7;
        else:
            self.averageLoadDeviationFitness = (self.averageLoadDeviationFitness - 0.7) / 0.3;
        
    def mutate(self):
        for i in range(24):
            if RandomNumberGenerator.uniform() < self.mutationRate and self.constraints[i] == 'x':
                self.chromosome[i] = RandomNumberGenerator.integers(1, 30)

    # STR
    def __str__(self):
        return f"{self.chromosome}: {self.totalScore}"