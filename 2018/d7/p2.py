import os
import re


# BASE_TASK_TIME = 0
# INPUT_FILE = 'test_input.txt'
# WORKERS = 2
BASE_TASK_TIME = 60
INPUT_FILE = 'input.txt'
WORKERS = 5


def test_instruct():
    return run_instruct() == 1115


def run_instruct():
    path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), INPUT_FILE)
    with open(path, 'r') as f:
        lines = f.read().splitlines()
    edges = parse_lines(lines)
    graph = Graph()
    populate_graph(graph, edges)
    steps = topo_sort(graph)

    manager = Manager(steps)
    done = False
    while not done:
        done = manager.work()

    return manager.seconds


class Vertex:
    def __init__(self, key):
        self.key = key
        self.state = 0
        self.parents = []
        self.edges = []
        self.priority = 0

    def add_neighbor(self, neighbor):
        self.edges.append(neighbor)

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.key)

    def get_time(self):
        return (ord(self.key) - 64) + BASE_TASK_TIME


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
                self.visit(edge)
            edge.parents.append(vertex)
        vertex.state = 2
        self.depth += 1
        vertex.priority = self.depth


class Worker:
    task = None
    time_left = 0

    def start_task(self, task):
        self.task = task
        self.time_left = task.get_time()

    def finish_task(self):
        self.task = None

    def work(self):
        self.time_left -= 1

    def is_done(self):
        return not self.time_left


class Manager:
    def __init__(self, tasks):
        self.workers = []
        for _ in range(WORKERS):
            self.workers.append(Worker())
        self.tasks = tasks
        self.completed_tasks = []
        self.seconds = 0

    def work(self):
        completed = []
        for worker in self.workers:
            if not worker.task:
                task = self.get_next_task()
                if task:
                    worker.start_task(task)
            if worker.task:
                worker.work()
                if worker.is_done():
                    completed.append(worker.task)
                    worker.finish_task()

        self.completed_tasks.extend(completed)
        self.seconds += 1
        return self.tasks == [] and all([w.is_done() for w in self.workers])

    def get_next_task(self):
        for task in self.tasks:
            if not task.parents or all([p in self.completed_tasks for p in task.parents]):
                self.tasks.remove(task)
                return task
        return None


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

