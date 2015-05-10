from random import randrange
from union_find import *
import operator

class Node(object):
    """
    Class that represents a node in a tree.
    """
    def __init__(self, label):
        self.label = label
        self.parent = None
        self.children = []

    def children():
        return self.children

    def add_child(self, node):
        node.parent = self
        self.children.append(node)

    def __str__(self):
        return str(self.label)

    def preorder(self, accumulator):
        accumulator.append(self.label)
        
        for child in self.children:
            if not child.label in accumulator:
                child.preorder(accumulator)

class Vertex(object):
    """
    Class that represents a vertex in a graph.
    """

    def __init__ (self, label):
        self.label = label

    def __str__(self):
        return self.label

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.label == other.label
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __hash__(self):
        return hash(self.label)

class Graph(object):
    """
    Class that represents a graph
    """

    def __init__(self, graph_adj_list={}):
        """ Initializes a graph object """
        self.graph_adj_list = graph_adj_list

    def vertices(self):
        """ Returns the vertices of a graph """
        return list(self.graph_adj_list.keys())

    def edges(self):
        """ Returns the edges of a graph """
        return self.__generate_edges()

    def add_vertex(self, vertex):
        """ 
        Adds a vextex to the graph. If the vertex "vertex" is not in 
        self.graph_adj_list, a key "vertex" with an empty
        list as a value is added to the dictionary. 
        Otherwise nothing has to be done. 
        
        Args:
            vertex: The object that represents the given new vertex.
        """
        if vertex not in self.graph_adj_list:
            self.graph_adj_list[vertex] = []

    def add_edge(self, edge):
        """
        Adds an edge to the graph. assumes that edge is of type set, tuple or list

        Args:
            edge: Set, tuple or list that represents the edge between two vertex.
        """
        edge = set(edge)
        (vertex1, vertex2) = tuple(edge)
        if vertex1 in self.graph_adj_list:
            self.graph_adj_list[vertex1].append(vertex2)
        else:
            self.graph_adj_list[vertex1] = [vertex2]

        if vertex2 in self.graph_adj_list:
            self.graph_adj_list[vertex2].append(vertex1)
        else:
            self.graph_adj_list[vertex2] = [vertex1]

    def __generate_edges(self):
        """ A static method generating the edges of the 
            graph "graph". Edges are represented as sets 
            with one (a loop back to the vertex) or two 
            vertices 
        """
        edges = []
        for vertex in self.graph_adj_list:
            for neighbour in self.graph_adj_list[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    def vertices_and_edges(self):
        """
        Returns a dict with the vertices from the graph and
        a list with the edges of the graph. The vertices are
        represented using the Vertex class.
        """
        tedges = []
        vertices = {}
        edges = []

        for vertex in self.graph_adj_list.keys():
            vertices[vertex] = Vertex(vertex)

        for vertex in self.graph_adj_list:
            for neighbour in self.graph_adj_list[vertex]:
                
                if {neighbour, vertex} not in tedges:
                    tedges.append({vertex, neighbour})
                    edges.append({vertices[vertex], vertices[neighbour]})

        return (vertices, edges)

    def __str__(self):
        res = "vertices: "
        for k in self.graph_adj_list:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res

    def approx_vertex_cover(self):
        """
        Approximation algorithm to construct a near-optimal vertex cover
        for an undirected graph. Algorithm from Cormen 2ed (pag 1024)

        Returns:
            A list with the near-optimal vertex cover for the graph.
        """
        # Initial cover is empty
        vertex_cover = []
        # A copy of the edges of the original graph
        edges = self.edges()

        # We loop while there is an edge
        while(len(edges) != 0):
            # We select an random edge.
            random_index = randrange(0, len(edges))
            edge = edges.pop(random_index)

            # We get the vertex of the choosen edge
            (vertex_u, vertex_v) = tuple(edge)

            # We add this vertex to the cover
            vertex_cover.append(vertex_u)
            vertex_cover.append(vertex_v)

            # Remove edges that are incident to vertex_u and/or vertex_v
            edges = [edge for edge in edges if (not vertex_u in edge) and (not vertex_v in edge)]

        return vertex_cover

    def kruskal(self, weighs):
        """
        Implementation of Kruskal algorithm to calculate the Minimum Spanning Tree
        of a graph.

        Args:
            A dict that has as keys the tuples representing a given edge, and their weigh as the value

        Returns:
            A list with the near-optimal vertex cover for the graph.
        """
        mst = []
        (vertices, edges) = self.vertices_and_edges()

        for label, vertex in vertices.iteritems():
            MakeSet(vertex)

        weighs = sorted(weighs.items(), key=operator.itemgetter(1))
        for (edge, weigh) in weighs:
            (vertex_u, vertex_v) = tuple(edge)
            if Find(vertices[vertex_u]) != Find(vertices[vertex_v]):
                mst.append(edge)
                Union(vertices[vertex_u], vertices[vertex_v])

        return mst

    def approx_tsp_tour(self, weighs):
        """
        Implementation of the approximation algorithm to calculate a near-optimal
        tour for a TSP problem

        Args:
            A dict that has as keys the tuples representing a given edge, and their weigh as the value

        Returns:
            A list with the near-optimal tour for the given graph
        """
        # Calculate the MST for the graph
        mst = sorted(self.kruskal(weighs))

        # Initialize tour
        tour = []

        # Create a node for each vertex
        nodes = {}
        for vertex in self.vertices():
            nodes[vertex] = Node(vertex)

        # From the edges of the MST create the corresponding tree.
        for edge in mst:
            (vertex_u, vertex_v) = edge

            parent = nodes[vertex_u]
            child = nodes[vertex_v]
            parent.add_child(child)
            child.add_child(parent)
                
        root = nodes[self.vertices()[0]]

        # Get the preorder walk of the tree, that is our tour
        result = []
        root.preorder(result)
        return result

if __name__ == "__main__":
    # Example graph from Cormen (page 1025)
    g = { "a" : ["b"],
          "b" : ["a", "c"],
          "c" : ["b", "e", "d"],
          "d" : ["c", "e", "f", "g"],
          "e" : ["c", "d", "f"],
          "f" : ["d", "e"],
          "g" : ["d"]
        }

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
        ("b", "c"): 1.41, ("b", "d"): 2.82, ("b", "e"): 3.16, ("b", "f"): 2, ("b", "g"): 4, ("b", "h"): 2.23,
        ("c", "d"): 4.24, ("c", "e"): 4.47, ("c", "f"): 3.16, ("c", "g"): 5.09, ("c", "h"): 2.23,
        ("d", "e"): 1.41, ("d", "f"): 2, ("d", "g"): 2.82, ("d", "h"): 4.12,
        ("e", "f"): 1.41, ("e", "g"): 1.41, ("e", "h"): 3.60,
        ("f", "g"): 2, ("f", "h"): 2.23,
        ("g", "h"): 3.60
    }


    graph = Graph(g)

    print "Graph G"
    print graph

    print "Approx Vertex Cover: %s" % graph.approx_vertex_cover()

    graph2 = Graph(g2)

    print "Graph G2"
    print graph2

    print "Kruskal: %s" % graph2.kruskal(g2_weighs)
    print "Approx TSP tour: %s" % graph2.approx_tsp_tour(g2_weighs)
