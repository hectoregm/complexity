from random import randrange
import random
from copy import copy
from operator import itemgetter, attrgetter, methodcaller

class GeneticIndividual(object):

    def __init__(self, cities, weighs, tour):
        self.cities = cities
        self.size = len(self.cities)
        self.weighs = weighs
        self.tour = tour

    def fitness(self):
        total = 0
        for idx in range(self.size):
            orig_city = self.tour[idx]
            if (idx + 1) == self.size:
                dst_city = self.tour[0]
            else:
                dst_city = self.tour[idx+1]

            total += self.weighs[(orig_city, dst_city)]

        return total

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

    def selection(size, selection_type="natural"):
        pass #for idx in range(size):

    def __str__(self):
        result = ""
        for individual in sorted(self.population, key=methodcaller('fitness')):
            result += str(individual.tour)
            result += ": " + str(individual.fitness()) + "\n"

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
    #import tsp_graph
    #graph, weighs = tsp_graph.generate_tsp_graph(5, 20)
    #print graph
    #print weighs

    g2 = { "a" : ["b", "c", "d", "e", "f", "g", "h"],
           "b" : ["a", "c", "d", "e", "f", "g", "h"],
           "c" : ["a", "b", "d", "e", "f", "g", "h"],
           "d" : ["a", "b", "c", "e", "f", "g", "h"],
           "e" : ["a", "b", "c", "d", "f", "g", "h"],
           "f" : ["a", "b", "c", "d", "e", "g", "h"],
           "g" : ["a", "b", "c", "d", "e", "f", "h"],
           "h" : ["a", "b", "c", "d", "e", "f", "g"]
    }

    # Example graph from Cormen (page 1029)
    g2_weighs = {
        ("a", "b"): 2, ("a", "c"): 3.16, ("a", "d"): 2, ("a", "e"): 3.16, ("a", "f"): 2.82, ("a", "g"): 4.47, ("a", "h"): 4.12,
        ("b", "a"): 2, ("b", "c"): 1.41, ("b", "d"): 2.82, ("b", "e"): 3.16, ("b", "f"): 2, ("b", "g"): 4, ("b", "h"): 2.23,
        ("c", "a"): 3.16, ("c", "b"): 1.41, ("c", "d"): 4.24, ("c", "e"): 4.47, ("c", "f"): 3.16, ("c", "g"): 5.09, ("c", "h"): 2.23,
        ("d", "a"): 2, ("d", "b"): 2.82, ("d", "c"): 4.24, ("d", "e"): 1.41, ("d", "f"): 2, ("d", "g"): 2.82, ("d", "h"): 4.12,
        ("e", "a"): 3.16, ("e", "b"): 3.16, ("e", "c"): 4.47, ("e", "d"): 1.41, ("e", "f"): 1.41, ("e", "g"): 1.41, ("e", "h"): 3.60,
        ("f", "a"): 2.82, ("f", "b"): 2, ("f", "c"): 3.16, ("f", "d"): 2, ("f", "e"): 1.41, ("f", "g"): 2, ("f", "h"): 2.23,
        ("g", "a"): 4.47, ("g", "b"): 4, ("g", "c"): 5.09, ("g", "d"): 2.82, ("g", "e"): 1.41, ("g", "f"): 2, ("g", "h"): 3.60,
        ("h", "a"): 4.12, ("h", "b"): 2.23, ("h", "c"): 2.23, ("h", "d"): 4.12, ("h", "e"): 3.60, ("h", "f"): 2.23, ("h", "g"): 3.60
    }
    
    tsp_solver = GeneticTSP(g2, g2_weighs)
    print tsp_solver
