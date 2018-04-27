import collections

class Graph:
    
    def __init__(self):
        
        #vertices/nodes are all the airports
        self.vertices= set()
        self.edges = collections.defaultdict(list)
        self.weights = {}
    
    
    def add_vertex(self,value):
        self.vertices.add(value)

    
    def add_edge(self, from_vertex, to_vertex, distance): 
        if from_vertex == to_vertex:
            pass
        
        self.edges[from_vertex].append(to_vertex)
        self.weights[(from_vertex, to_vertex)] = distance
        

    def __str__(self):
        string = "vertices: " + str(self.vertices) + "\n"
        string += "edges: " + str(self.edges) + "\n"
        string += "weights: " + str(self.weights)
        return string

#http://interactivepython.org/runestone/static/pythonds/BasicDS/ImplementingaQueueinPython.html
class Queue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()
        

    def size(self):
        return len(self.items)