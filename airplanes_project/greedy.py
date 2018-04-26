from data_structures import Graph
from data_structures import Queue
import csv


class GreedyItinery():
    
    def __init__(self,aircraftPass,atlasObj):
        
        ''' this method initalized an instance of the Itinerary class '''
        
        self.aircraftPass = aircraftPass
        self.atlasObj = atlasObj
            

    def findBestRoute(self, inputCSV):
        
        ''' This method is the centralhub of the bestRoute file and it drives 
        the methods that find the best route and then writes them to a file '''
        
        directed_graph = Graph() # Creating an Instance of the Graph class defined in data structures file
        filename = "./data/BestRoutesGreedy.csv" #https://stackoverflow.com/questions/12277864/python-clear-csv-file. truncates the file if data already exists in it
        f = open(filename, "w+")
        f.close()
        
        writeToFileList = [["Origin","Dest1","Dest2","Dest3","Dest4","Home","Cost","Aircraft"]]
        self.inputSet = [] #needs to be a list because aircraft is included
        self.inputCSV = inputCSV
         
        with open(self.inputCSV) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')  #takes each cell in the csv file
            for line in readCSV:
                RouteCostForFile= [] 
                aircraft, vertices = self.createVertices(line) #find the aircrafts and the different airports
                print("===============================================================================")
                print("You have requested the best route for", vertices, " using aircraft:", aircraft)
                
                if len(aircraft)>0: # if there is an airport present
                    self.addVerticesToGraph(vertices,directed_graph) # creating the vertices of the graph
                    self.addEdgestoGraph(vertices,directed_graph)  #adds the edges to the graph
                    path, total_cost = self.findShortestPath(directed_graph,vertices,aircraft) # collect the return path and cost

                    
                    if path.size() == 6: #checking that the path is length of 6 otherwise the journey wasnt completed
                        while path.size() > 0: # loop until all finished
                            city = path.dequeue() #remove the first element entered into the queue
                            print(city, end= ' ') #print the dequeued element
                            print('--->', end = ' ')
                            RouteCostForFile.append(city) #add the route to a list 
                        print('Total cost is: €',total_cost) # print the cost
                        RouteCostForFile.append(total_cost)
                        RouteCostForFile.append(aircraft) # preparing to write list to file
                        writeToFileList.append(RouteCostForFile) #writing the route to file 
                    
                    else:
                        print("The journey could not be completed")
    
        
            with open('./data/BestRoutesGreedy.csv', "a") as csv_file:
                writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
                for line in writeToFileList:
                    writer.writerow(line)
            #https://stackoverflow.com/questions/2084069/create-a-csv-file-with-values-from-a-python-list    
                
    def createVertices(self,line):
        
        ''' this function returns the aircraft(if it exsists) and list of cities '''
        self.vertices = line #the line thats read in
        
        if len(self.vertices) == 5: #error handling. if there is no aircraft given then it just returns the route 
            return '',self.vertices
        
        elif len(self.vertices) == 6:
            self.aircraft = self.vertices[-1] #aircraft is the last element in the route.
            self.vertices = self.vertices[:-1] # this is the remaining elements of the line read in
            return self.aircraft, self.vertices
        else:
            print("There is an error in the input. It does not input the correct number of airports and/or aircrafts")
        
        
    def addVerticesToGraph(self,vertices,graph):
        
        ''' This function accepts the different cities to be visited. It loops through them and creates 
        nodes in a graph. '''
        self.vertices = vertices
        for v in self.vertices: 
            graph.add_vertex(v) #the vertices are added to a set in the graph class

            
    
    def addEdgestoGraph(self,cities,graph):
        
        '''This function accepts the cities and a graph containing these cities and it adds links 
        between each city present in the graph with a weight of the cost of the trip'''
        
        self.cities = cities 
        for i in self.cities:
            for j in self.cities:
                if i != j: #this because dont need to link cities to themselves.

                    cost = self.atlasObj.getCostOfTrip(i, j) #cost of the trip is added as weight on the edges
                    graph.add_edge(i, j, cost) #adds the edges between nodes


                
    def findShortestPath(self,graph,vertices,aircraft):
        
        ''' this function accepts the graph containing nodes and weighted edges between them, the list of cities to be 
         visted and the aircraft to be used in the itinery and finds the shortest path if possible'''
        
        current_city = vertices[0] #this is the first city
        next_city_to_visit = current_city # setting this as a trap if no cloest city is found
        original_start = current_city #original current_city needed for later on
        path = Queue() #Queue to store the best path
        path.enqueue(current_city) #adding the starting node to the best path 
        total_cost =0 # initalizing the total cost to 0
        vertices.remove(current_city) #removing the starting point from the list of cities
    
        while len(vertices) > 0 : #while there are still cities to be visited
            shortest_distance = 9999999999 
            
            for elem in vertices: # for each remaining city in the list of cities
                distance = self.atlasObj.getDistanceBetweenAirports(current_city,elem) #get the distance from the last city to this new one
                if graph.weights[current_city,elem] < shortest_distance and self.aircraftPass.airplanePassFuel(distance,aircraft): #Check the distance is shorter and the aircraft can complete the journey
                        shortest_distance = graph.weights[current_city,elem] #new shortest distance    
                        next_city_to_visit = elem #next city to visit is this one
                      
                else: #if its not shorter than the current shortest or it doesnt pass the fuel check then continue to next airport
                    continue
            
            if current_city == next_city_to_visit: # this would mean that the journey cant be completed as next one isnt found
                return path, "cant complete trip"
            
            else:
                path.enqueue(next_city_to_visit) #add the next city to visit to the path 
                total_cost += graph.weights[current_city,next_city_to_visit] #add the cost of this to the 
                current_city = next_city_to_visit #the next city to visit becomes the current city for the next leg
                vertices.remove(next_city_to_visit) #remove the city to be visited from the list of remaining cities
             
        # this will only be reached if the full path was made as it wouldve been returned earlier if not 
        last_stop = next_city_to_visit #the last city to visit before heading home
        path.enqueue(original_start) #add the original starting point to the queue 
        
        if (self.aircraftPass.airplanePassFuel(self.atlasObj.getDistanceBetweenAirports(last_stop,original_start),aircraft)): # check that the last stop to the starting point can be done
            total_cost += graph.weights[last_stop, original_start] # adding the cost the the toal cost 
            return path, total_cost #return the path and total cost
        
        else:
            return path, "cant complete trip" # if the plane cant complete the journey






