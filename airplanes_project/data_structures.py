import collections

#adapted from lab 7
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
        self.unordered_queue = UnorderedList()

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.unordered_queue.add(item)

    def dequeue(self):
        temp = self.unordered_queue.returnLast()
        self.unordered_queue.remove(temp)
        return temp
    
    def size(self):
        return self.unordered_queue.size()
    

#Adapted from: http://interactivepython.org/runestone/static/pythonds/BasicDS/ImplementinganUnorderedListLinkedLists.html
class Node:
    def __init__(self,initdata):
        self.data = initdata
        self.next = None

    def getData(self):
        return self.data

    def getNext(self):
        return self.next

    def setData(self,newdata):
        self.data = newdata

    def setNext(self,newnext):
        self.next = newnext


class UnorderedList:

    def __init__(self):
        self.head = None

    def isEmpty(self):
        return self.head == None

    def add(self,item):
        temp = Node(item)
        temp.setNext(self.head)
        self.head = temp

    def size(self):
        current = self.head
        count = 0
        while current != None:
            count = count + 1
            current = current.getNext()

        return count

    def search(self,item):
        current = self.head
        found = False
        while current != None and not found:
            if current.getData() == item:
                found = True
            else:
                current = current.getNext()

        return found

    def remove(self,item):
        current = self.head
        previous = None
        found = False
        while not found:
            if current.getData() == item:
                found = True
            else:
                previous = current
                current = current.getNext()

        if previous == None:
            self.head = current.getNext()
        else:
            previous.setNext(current.getNext())
    
    def returnLast(self):
        
        temp = self.head
        while(temp.next is not None):
            temp = temp.next
        return temp.getData()