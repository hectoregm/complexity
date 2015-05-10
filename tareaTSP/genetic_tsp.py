from random import randrange
import random
from copy import copy

class GeneticIndividual(object):

    def __init__(self, cities, weighs, tour):
        self.cities = cities
        self.weighs = weighs
        self.tour = tour

    @classmethod
    def random(cls, cities, weighs):
        tour = copy(cities)
        random.shuffle(tour)
        
        return cls(cities, weighs, tour)
        

class GeneticPopulation(object):

    def __init__(self, graph, weighs, population_size, generate=True):
        self.population = []
        self.cities = graph.keys()

        if generate:
            for individual in range(0, population_size):
                self.population.append(GeneticIndividual.random(self.cities, weighs))

    def __str__(self):
        result = ""
        for individual in self.population:
            result += str(individual.tour) + "\n"

        return result

class GeneticTSP(object):

    def __init__(self, graph, weighs, population=20, generations=500):
        self.graph = graph
        self.weighs = weighs
        self.psize = population
        self.generations = generations

        self.population = GeneticPopulation(self.graph, self.weighs, self.psize)

    def solve(self):
        return []

    def __str__(self):
        result = "Possible solutions (Tours):\n"
        result += str(self.population)

        return result
        

if __name__ == "__main__":
    import tsp_graph
    graph, weighs = tsp_graph.generate_tsp_graph(5, 20)
    print graph
    print weighs

    tsp_solver = GeneticTSP(graph, weighs)
    print tsp_solver
