from multiprocessing import Pool
import numpy as np

from .RandomNumberGenerator import RandomNumberGenerator
from .Simulation import Simulation
from .models import TimeTable


class Genetics:
    # INIT
    def __init__(self, populationSize, mutationRate, maxConnectionsPerHour, vehicleCapacity, vehicleSeats, costPerSeatKm, routeLength, busStops, constraints):
        self.populationSize = populationSize
        self.mutationRate = mutationRate
        self.maxConnectionsPerHour = maxConnectionsPerHour
        self.vehicleCapacity = vehicleCapacity
        self.vehicleSeats = vehicleSeats
        self.costPerSeatKm = costPerSeatKm
        self.routeLength = routeLength
        self.busStops = busStops
        self.constraints = constraints
        self.generation = []
        self.offsprings = []
        self.initPopulation()
        self.fronts = []

    # METHODS
    def initPopulation(self):
        for i in range(self.populationSize):
            self.generation.append(Individual(self.mutationRate, self.maxConnectionsPerHour, self.vehicleCapacity, self.vehicleSeats, self.costPerSeatKm, self.routeLength, self.busStops, self.constraints))
        self.nonDominatedSort()
        for front in self.fronts:
            self.crowdingDistanceAssignment(front)
        self.makeNewPopulation()
        
    def updateGeneration(self):
        self.generation += self.offsprings
        self.nonDominatedSort()
        self.generation = []
        i = 0
        while len(self.generation) + len(self.fronts[i]) <= self.populationSize:
            self.crowdingDistanceAssignment(self.fronts[i])
            self.generation += self.fronts[i]
            i += 1
        self.fronts[i].sort()
        for individual in self.fronts[i]:
            if len(self.generation) >= self.populationSize:
                break
            self.generation.append(individual)
        self.makeNewPopulation()

    def makeNewPopulation(self):
        self.offsprings = []
        for _ in range(int(self.populationSize/2)):
            parent1 = self.parentSelection()
            parent2 = self.parentSelection()
            child1, child2 = self.crossover(parent1, parent2)
            self.offsprings.append(child1)
            self.offsprings.append(child2)

    def parentSelection(self):
        parent1 = self.generation[RandomNumberGenerator.integers(0, len(self.generation))]
        parent2 = self.generation[RandomNumberGenerator.integers(0, len(self.generation))]
        if parent1 < parent2:
            return parent1
        return parent2

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
        return Individual(self.mutationRate, self.maxConnectionsPerHour, self.vehicleCapacity, self.vehicleSeats, self.costPerSeatKm, self.routeLength, self.busStops, self.constraints, newChromosome1), Individual(self.mutationRate, self.maxConnectionsPerHour, self.vehicleCapacity, self.vehicleSeats, self.costPerSeatKm, self.routeLength, self.busStops, self.constraints, newChromosome2)

    def nonDominatedSort(self):
        self.fronts = []
        self.fronts.append([])
        for p in self.generation:
            p.dominatesOver = []
            p.dominationCount = 0
            for q in self.generation:
                if p.constraintDominates(q):
                    p.dominatesOver.append(q)
                elif q.constraintDominates(p):
                    p.dominationCount +=1
            if p.dominationCount == 0:
                p.rank = 1
                self.fronts[0].append(p)
        i = 0
        while len(self.fronts[i]) > 0:
            nextFront = []
            for p in self.fronts[i]:
                for q in p.dominatesOver:
                    q.dominationCount -= 1
                    if q.dominationCount == 0:
                        q.rank = i+1
                        nextFront.append(q)
            i += 1
            self.fronts.append(nextFront)
        self.fronts.pop(-1)

    def crowdingDistanceAssignment(self, front):
        length = len(front)
        for individual in front:
            individual.distance = 0
        
        front = sorted(front, key=lambda individual: individual.cost)
        min = front[0].cost
        max = front[length - 1].cost
        front[0].distance = front[length-1].distance = float('inf')
        for i in range(1, length - 2):
            front[i].distance += (front[i+1].cost - front[i-1].cost) / (max - min)

        front = sorted(front, key=lambda individual: individual.satisfaction)
        min = front[0].satisfaction
        max = front[length - 1].satisfaction
        front[0].distance = front[length-1].distance = float('inf')
        for i in range(1, length - 2):
            front[i].distance += (front[i+1].satisfaction - front[i-1].satisfaction) / (max - min)
    # STR
    def __str__(self):
        output = ""
        for individual in self.generation:
            output += f"{individual}\n"
        return output

class Individual:
    # INIT
    def __init__(self, mutationRate, maxConnectionsPerHour, vehicleCapacity, vehicleSeats, costPerSeatKm, routeLength, busStops, constraints, chromosome=None):
        self.mutationRate = mutationRate
        self.maxConnectionsPerHour = maxConnectionsPerHour
        self.vehicleCapacity = vehicleCapacity
        self.vehicleSeats = vehicleSeats
        self.costPerSeatKm = costPerSeatKm
        self.routeLength = routeLength
        self.busStops = busStops
        self.constraints = constraints
        if chromosome is None:
            self.chromosome = self.generateRandomChromosome()
        else:
            self.chromosome = chromosome
        self.mutate()
        self.calculateFitness()
        self.dominatesOver = []
        self.dominationCount = 0
        self.rank = 0
        self.distance = 0
        self.totalPassengersLeftUnboarded = 0

    # METHODS
    def generateRandomChromosome(self):
        chromosome = []
        for i in range(24):
            if self.constraints[i] == None:
                chromosome.append(RandomNumberGenerator.integers(1, self.maxConnectionsPerHour+1))
            else:
                chromosome.append(self.constraints[i])
        return chromosome

    def calculateFitness(self):
        self.cost = 0
        self.satisfaction = 0
        timeTable = TimeTable(self.chromosome)
        stats = Simulation.run(0, 24*60, self.busStops, timeTable, self.vehicleCapacity, self.vehicleSeats)
        self.cost = (self.routeLength * stats.totalNumberOfBuses * self.vehicleCapacity / 100 * self.costPerSeatKm)
        self.satisfaction = stats.averagePassengerSatisfaction
        self.totalPassengersLeftUnboarded = stats.busStopStatistics.totalPassengersLeftUnboarded

    def constraintDominates(self, other):
        if self.totalPassengersLeftUnboarded == 0 and other.totalPassengersLeftUnboarded == 0:
            return self.dominates(other)
        else:
            return self.totalPassengersLeftUnboarded < other.totalPassengersLeftUnboarded

    def dominates(self, other) -> bool:
        return (self.cost <= other.cost and self.satisfaction >= other.satisfaction) and (self.cost < other.cost or self.satisfaction > other.satisfaction)
        
    def mutate(self):
        for i in range(24):
            if RandomNumberGenerator.uniform() < self.mutationRate and self.constraints[i] == None:
                self.chromosome[i] = RandomNumberGenerator.integers(1, self.maxConnectionsPerHour+1)
            
    def __lt__(self, other):
        return (self.rank < other.rank) or ((self.rank == other.rank) and (self.distance > other.distance))

    # STR
    def __str__(self):
        return f"{self.chromosome}: {self.fitness}"