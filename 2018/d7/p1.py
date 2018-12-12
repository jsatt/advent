import os
import re


def test_instruct():
    return run_instruct() == 'GRTAHKLQVYWXMUBCZPIJFEDNSO'


def run_instruct():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "input.txt")
    with open(path, 'r') as f:
        lines = f.read().splitlines()
    edges = parse_lines(lines)
    graph = Graph()
    populate_graph(graph, edges)
    steps = topo_sort(graph)
    return ''.join([s.key for s in steps])


class Vertex:
    def __init__(self, key):
        self.key = key
        self.state = 0
        self.parent = None
        self.edges = []
        self.priority = 0

    def add_neighbor(self, neighbor):
        self.edges.append(neighbor)

    def __repr__(self):
        return '<{}: {}, {}, {}>'.format(self.__class__.__name__, self.key, self.priority, self.parent)


class Graph:
    def __init__(self):
        self.vertices = {}
        self.depth = 0

    def add_edge(self, start, end):
        if start not in self.vertices:
            self.vertices[start] = Vertex(start)
        if end not in self.vertices:
            self.vertices[end] = Vertex(end)
        self.vertices[start].add_neighbor(self.vertices[end])

    def dfs(self):
        for vertex in sorted(self.vertices.values(), key=lambda x: x.key, reverse=True):
            if vertex.state == 0:
                self.visit(vertex)

    def visit(self, vertex):
        vertex.state = 1
        self.depth += 1
        for edge in sorted(vertex.edges, key=lambda x: x.key, reverse=True):
            if edge.state == 0:
                edge.parent = vertex
                self.visit(edge)
        vertex.state = 2
        self.depth += 1
        vertex.priority = self.depth


def parse_lines(lines):
    regex = re.compile('Step (.) must be finished before step (.) can begin.')
    for line in lines:
        yield regex.search(line).groups()


def populate_graph(graph, edges):
    for start, end in edges:
        graph.add_edge(start, end)


def topo_sort(graph):
    graph.dfs()
    vertices = list(graph.vertices.values())
    vertices.sort(key=lambda v: v.priority, reverse=True)
    return vertices
