from multiprocessing import Pool
import numpy as np

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
        self.bestIndividual = None
        self.initPopulation(initialChromosome)

    # METHODS
    def initPopulation(self, initialChromosome=None):
        for i in range(self.populationSize):
            self.generation.append(Individual(self.mutationRate, self.busStops, self.constraints))

        if initialChromosome is not None:
            self.generation.pop(0)
            self.generation.append(Individual(self.mutationRate, self.busStops, self.constraints, initialChromosome))

        self.generation = Pool().map(self.calculateFitnessWrapper, self.generation)
            
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
        parent1 = self.generation[RandomNumberGenerator.integers(0, len(self.generation))]
        parent2 = self.generation[RandomNumberGenerator.integers(0, len(self.generation))]
        if parent1.fitness > parent2.fitness:
            return parent1
        return parent2
        
    def updateGeneration(self):
        newGeneration = []

        for i in range(self.elitismCount):
            newGeneration.append(self.generation[i])

        filteredGeneration = list(filter(lambda x: x.fitness > 0, self.generation))
        if len(filteredGeneration) >= 2:
            self.generation = filteredGeneration

        for i in range(int((self.populationSize - self.elitismCount)/2)):
            parent1 = self.parentSelection()
            parent2 = self.parentSelection()
            child1, child2 = self.crossover(parent1, parent2)
            child1.mutate()
            child2.mutate()
            newGeneration.append(child1)
            newGeneration.append(child2)
                
        self.generation = newGeneration

        self.generation = Pool().map(self.calculateFitnessWrapper, self.generation)

        self.sortGeneration()
    
    def calculateFitnessWrapper(self, individual):
        individual.calculateFitness()
        return individual

    def sortGeneration(self):
        self.generation.sort(key=lambda x: x.fitness, reverse=True)
        if self.bestIndividual is None or self.generation[0].fitness > self.bestIndividual.fitness:
            self.bestIndividual = self.generation[0]


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
        self.fitness = 0

    # METHODS
    def generateRandomChromosome(self):
        chromosome = []
        for i in range(24):
            if self.constraints[i] == 'x':
                chromosome.append(RandomNumberGenerator.integers(1, 15))
            else:
                chromosome.append(self.constraints[i])
        return chromosome

    def calculateFitness(self):
        self.fitness = 0
        timeTable = TimeTable(self.chromosome)
        stats = Simulation.run(0, 24*60, self.busStops, timeTable)
        self.fitness -= round(stats.totalNumberOfBuses * stats.busStatistics.capacity)
        self.fitness += stats.busStatistics.totalPassengersTransported
        self.fitness -= stats.busStopStatistics.totalPassengersWaitingForNextBus
        self.fitness -= stats.busStopStatistics.totalTimeSpentWaiting / stats.busStopStatistics.totalPassengersArrived
        
        if stats.busStopStatistics.totalPassangersLeftUnboarded != 0:
            self.fitness = -1000000
        
    def mutate(self):
        for i in range(24):
            if RandomNumberGenerator.uniform() < self.mutationRate and self.constraints[i] == 'x':
                self.chromosome[i] = RandomNumberGenerator.integers(1, 15)

    # STR
    def __str__(self):
        return f"{self.chromosome}: {self.fitness}"