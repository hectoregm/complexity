from random import randrange
from copy import copy
import math

def create_coordinates(order, grid_size):
    coords = []

    count = 0

    while count < order:
        x_coord = randrange(grid_size)
        y_coord = randrange(grid_size)

        if not (x_coord, y_coord) in coords:
            coords.append((x_coord, y_coord))
            count += 1

    return coords

def generate_tsp_graph(order, grid_size):
    coords = create_coordinates(order, grid_size)

    graph = {}
    weighs = {}
    vertices = range(1, order + 1)

    for index_from, coord in enumerate(coords, start=1):
        for index_to, other in enumerate(coords, start=1):
            if index_from == index_to:
                continue

            distance = math.sqrt(abs(coord[0] - other[0])** 2 + abs(coord[1] - other[1])**2)
            weighs[(index_from, index_to)] = distance

        tmp_vertices = copy(vertices)
        tmp_vertices.remove(index_from)
        graph[index_from] = tmp_vertices

    return (graph, weighs)

if __name__ == "__main__":
    graph, weight = generate_tsp_graph(3, 10)
    print graph
    print weight
    
