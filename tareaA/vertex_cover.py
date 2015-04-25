from random import randrange

class Graph(object):

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

    def __str__(self):
        res = "vertices: "
        for k in self.graph_adj_list:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res

    def approx_vertex_cover(self):
        vertex_cover = []
        edges = self.edges()

        while(len(edges) != 0):
            random_index = randrange(0, len(edges))
            edge = edges.pop(random_index)
            (vertex_u, vertex_v) = tuple(edge)

            vertex_cover.append(vertex_u)
            vertex_cover.append(vertex_v)

            temp = []
            for edge in edges:
                if (not vertex_u in edge) and (not vertex_v in edge):
                    temp.append(edge)

            edges = temp

        return vertex_cover

if __name__ == "__main__":

    
    g = { "a" : ["b"],
          "b" : ["a", "c"],
          "c" : ["b", "e", "d"],
          "d" : ["c", "e", "f", "g"],
          "e" : ["c", "d", "f"],
          "f" : ["d", "e"],
          "g" : ["d"]
        }


    graph = Graph(g)

    print("Vertices of graph:")
    print(graph.vertices())

    print("Edges of graph:")
    print(graph.edges())

    print graph

    print graph.approx_vertex_cover()
