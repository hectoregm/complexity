from random import randrange
import random
import math
from copy import copy
from operator import methodcaller
import approx_algorithms as ap

def get_values(n, blacklist, array):
    count = 0
    index = 0
    result = []

    while count < n:
        if array[index] in blacklist:
            index += 1
            continue
        else:
            result.append(array[index])
            index += 1
            count += 1

    return result

def get_values_order(index, blacklist, array):
    result = []

    length = len(array)

    for idx in range(length):
        rindex = (index + idx) % length
        if not array[rindex] in blacklist:
            result.append(array[rindex])

    return result

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

            weigh = self.weighs.get((orig_city, dst_city), False)
            if weigh:
                total += self.weighs[(orig_city, dst_city)]
            else:
                total += self.weighs[(dst_city, orig_city)]

        return total

    def crossover(self, other, cross_type="partial"):
        if cross_type == "one_point":
            cutpoint = random.randrange(self.size)
            new_tour_one = self.tour[0:cutpoint] + other.tour[cutpoint:]

            cities = {}
            gaps = []
            repeated_cities = []
            for idx in range(self.size):
                if cities.get(new_tour_one[idx], False):
                    gaps.append(idx)
                    repeated_cities.append(new_tour_one[idx])
                else:
                    cities[new_tour_one[idx]] = 1

            if len(gaps) > 0:
                values = get_values(len(gaps), cities.keys(), other.tour)
                for idx in range(len(gaps)):
                    new_tour_one[gaps[idx]] = values[idx]

            new_tour_two = other.tour[0:cutpoint] + self.tour[cutpoint:]

            cities = {}
            gaps = []
            repeated_cities = []
            for idx in range(self.size):
                if cities.get(new_tour_two[idx], False):
                    gaps.append(idx)
                    repeated_cities.append(new_tour_two[idx])
                else:
                    cities[new_tour_two[idx]] = 1

            if len(gaps) > 0:
                values = get_values(len(gaps), cities.keys(), self.tour)
                for idx in range(len(gaps)):
                    new_tour_two[gaps[idx]] = values[idx]

        elif cross_type == "partial":
            msize = 3
            index = random.randrange(self.size-msize+1)
            submatch_a = self.tour[index:index + msize]
            submatch_b = other.tour[index:index + msize]

            new_tour_one = [0] * self.size
            new_tour_two = [0] * self.size

            blacklist_one = copy(submatch_a)
            for idx in range(self.size):
                if ((idx < index) or idx >= (index + msize)) and not other.tour[idx] in submatch_a:
                    new_tour_one[idx] = other.tour[idx]

            blacklist_two = copy(submatch_b)
            for idx in range(self.size):
                if ((idx < index) or idx >= (index + msize)) and not self.tour[idx] in submatch_b:
                    new_tour_two[idx] = self.tour[idx]
            
            new_tour_one[index:index + msize] = submatch_a
            new_tour_two[index:index + msize] = submatch_b

            missing = [node for node in submatch_b if not node in new_tour_one]
            count = 0
            if len(missing) > 0:
                for idx in range(self.size):
                    if new_tour_one[idx] == 0:
                        new_tour_one[idx] = missing[count]
                        count += 1

            missing = [node for node in submatch_a if not node in new_tour_two]
            count = 0
            if len(missing) > 0:
                for idx in range(self.size):
                    if new_tour_two[idx] == 0:
                        new_tour_two[idx] = missing[count]
                        count += 1
        elif cross_type == "order":
            msize = 3
            index = random.randrange(self.size-msize+1)
            submatch_a = self.tour[index:index + msize]
            submatch_b = other.tour[index:index + msize]

            new_tour_one = [0] * self.size
            new_tour_two = [0] * self.size
            
            new_tour_one[index:index + msize] = submatch_a
            new_tour_two[index:index + msize] = submatch_b

            missing = get_values_order(index, submatch_a, other.tour)
            count = 0
            if len(missing) > 0:
                for idx in range(self.size):
                    if new_tour_one[idx] == 0:
                        new_tour_one[idx] = missing[count]
                        count += 1

            missing = get_values_order(index, submatch_b, self.tour)
            count = 0
            if len(missing) > 0:
                for idx in range(self.size):
                    if new_tour_two[idx] == 0:
                        new_tour_two[idx] = missing[count]
                        count += 1

        return (GeneticIndividual(self.cities, self.weighs, new_tour_one),
                GeneticIndividual(self.cities, self.weighs, new_tour_two))

    def mutate(self, mutation_type="swap", psize=2):
        if mutation_type == "swap":
            index_a = random.randrange(self.size)
            index_b = random.randrange(self.size)
            temp = self.tour[index_b]
            self.tour[index_b] = self.tour[index_a]
            self.tour[index_a] = temp
        elif mutation_type == "insertion":
            index_a = random.randrange(self.size)
            index_b = random.randrange(self.size-1)
            value = self.tour.pop(index_a)
            self.tour.insert(index_b, value)
        elif mutation_type == "shift":
            index_a = random.randrange(self.size-psize+1)
            index_b = random.randrange(self.size-psize-psize+1)
            subpath = self.tour[index_a:index_a + psize]

            self.tour[index_a:index_a + psize] = []

            if index_b == 0:
                self.tour = subpath + self.tour
            else:
                self.tour[index_b:1] = subpath

    def __str__(self):
        return str(self.tour) + " cost: " + str(self.fitness())

    @classmethod
    def random(cls, cities, weighs):
        tour = copy(cities)
        random.shuffle(tour)
        
        return cls(cities, weighs, tour)
        

class GeneticPopulation(object):

    def __init__(self, graph, weighs, population_size, generate=True):
        self.graph = graph
        self.weighs = weighs
        self.size = population_size
        self.population = []
        self.cities = graph.keys()

        if generate:
            for individual in range(0, population_size):
                self.population.append(GeneticIndividual.random(self.cities, weighs))

    def selection(self, size, selection_type="natural"):
        self.population = sorted(self.population, key=methodcaller('fitness'))

        if selection_type == "natural":
            selection = GeneticPopulation(self.graph, self.weighs, size, False)
            selection.population = self.population[0:size]
        elif selection_type == "weight":
            num_elites = int(math.floor(size * 0.80))
            elites = self.population[0:num_elites]
            tails = self.population[:(num_elites-(size+1)):-1]

            selection = GeneticPopulation(self.graph, self.weighs, size, False)
            selection.population = elites + tails
        elif selection_type == "random":
            num_elites = int(math.floor(size * 0.50))
            winners = self.population[0:num_elites]

            while len(winners) < size:
                winner = self.population[random.randrange(self.size)]
                if not winner in winners:
                    winners.append(winner)
                else:
                    continue

            selection = GeneticPopulation(self.graph, self.weighs, size, False)
            selection.population = winners

        return selection

    def select(self):
        return self.population[random.randrange(self.size)]

    def elite(self):
        return sorted(self.population, key=methodcaller('fitness'))[0]

    def reproduce(self, cross_type="one_point", mutation_type="swap"):
        children = []
        for _ in range(self.size):
            parent_a = self.select()
            parent_b = self.select()

            child_a, child_b = parent_a.crossover(parent_b, cross_type)
            child_a.mutate()
            child_b.mutate()
            children.append(child_a)
            children.append(child_b)

        return children

    def __str__(self):
        result = ""
        for individual in sorted(self.population, key=methodcaller('fitness')):
            result += str(individual.tour)
            result += ": " + str(individual.fitness()) + "\n"

        return result

class GeneticTSP(object):

    def __init__(self, graph, weighs, population=25, generations=500):
        self.graph = graph
        self.weighs = weighs
        self.psize = population
        self.generations = generations
        self.selection_strategies = ["natural", "weight", "random"]
        self.cross_strategies = ["one_point", "partial", "order"]
        self.mutation_strategies = ["swap", "insertion", "shift"]

        self.population = GeneticPopulation(self.graph, self.weighs, self.psize)

    def select_strategies(self):
        selection = self.selection_strategies[random.randrange(3)]
        cross = self.cross_strategies[random.randrange(3)]
        mutation = self.mutation_strategies[random.randrange(3)]

        return (selection, cross, mutation)

    def solve(self):
        print "Solving..."

        for idx in range(self.generations):
            selection_strategy, cross_strategy, mutation_strategy = self.select_strategies()
            #print "Generation %d, using %s, %s, %s" % (idx, selection_strategy, cross_strategy, mutation_strategy)

            selection = self.population.selection(5, selection_strategy)
            children = selection.reproduce(cross_strategy, mutation_strategy)
            self.population.population += children

            self.population = self.population.selection(self.psize, selection_strategy)


        print "Best solution found (GA)"
        print self.population.elite()

    def __str__(self):
        result = "Possible solutions (Tours):\n"
        result += str(self.population)

        return result
        

if __name__ == "__main__":
    import tsp_graph

    cormen_graph = { "a" : ["b", "c", "d", "e", "f", "g", "h"],
           "b" : ["a", "c", "d", "e", "f", "g", "h"],
           "c" : ["a", "b", "d", "e", "f", "g", "h"],
           "d" : ["a", "b", "c", "e", "f", "g", "h"],
           "e" : ["a", "b", "c", "d", "f", "g", "h"],
           "f" : ["a", "b", "c", "d", "e", "g", "h"],
           "g" : ["a", "b", "c", "d", "e", "f", "h"],
           "h" : ["a", "b", "c", "d", "e", "f", "g"]
    }

    # Example graph from Cormen (page 1029)
    cormen_weighs = {
        ("a", "b"): 2, ("a", "c"): 3.16, ("a", "d"): 2, ("a", "e"): 3.16, ("a", "f"): 2.82, ("a", "g"): 4.47, ("a", "h"): 4.12,
        ("b", "c"): 1.41, ("b", "d"): 2.82, ("b", "e"): 3.16, ("b", "f"): 2, ("b", "g"): 4, ("b", "h"): 2.23,
        ("c", "d"): 4.24, ("c", "e"): 4.47, ("c", "f"): 3.16, ("c", "g"): 5.09, ("c", "h"): 2.23,
        ("d", "e"): 1.41, ("d", "f"): 2, ("d", "g"): 2.82, ("d", "h"): 4.12,
        ("e", "f"): 1.41, ("e", "g"): 1.41, ("e", "h"): 3.60,
        ("f", "g"): 2, ("f", "h"): 2.23,
        ("g", "h"): 3.60
    }

    print "Cormen TSP Example"
    tsp_solver = GeneticTSP(cormen_graph, cormen_weighs, 20)
    tsp_solver.solve()

    graph_approx = ap.Graph(cormen_graph)

    tour = graph_approx.approx_tsp_tour(cormen_weighs)
    print "Approx TSP tour: %s cost: %s" % (tour, GeneticIndividual(cormen_graph.keys(), cormen_weighs, tour).fitness())

    print "\nTSP instance, order = 50, poblation = 25, generations = 2000"
    graph, weighs = tsp_graph.generate_tsp_graph(50, 200)
    
    tsp_solver = GeneticTSP(graph, weighs, 25, 2000)
    tsp_solver.solve()

    graph_approx = ap.Graph(graph)

    tour = graph_approx.approx_tsp_tour(weighs)
    print "Approx TSP tour: %s cost: %s" % (tour, GeneticIndividual(graph.keys(), weighs, tour).fitness())

    print "\nTSP instance, order = 70, poblation = 35, generations = 4000"
    graph, weighs = tsp_graph.generate_tsp_graph(70, 200)
    
    tsp_solver = GeneticTSP(graph, weighs, 35, 4000)
    tsp_solver.solve()

    graph_approx = ap.Graph(graph)

    tour = graph_approx.approx_tsp_tour(weighs)
    print "Approx TSP tour: %s cost: %s" % (tour, GeneticIndividual(graph.keys(), weighs, tour).fitness())
