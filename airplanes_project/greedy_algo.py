from data_structures import Graph, Queue, UnorderedList
import csv


class GreedyItinery():
    
    def __init__(self,aircraft, atlas,currency,rate):
        
        ''' this method initalized an instance of the Itinerary class '''
        
        self.aircraft_obj = aircraft
        self.atlas_obj = atlas
        self.currency_obj = currency
        self.rate_obj = rate
        
            

    def findBestRoute(self, inputCSV):
        
        ''' This method is the centralhub of the bestRoute file and it drives 
        the methods that find the best route and then writes them to a file '''
        
        directed_graph = Graph() # Creating an Instance of the Graph class defined in data structures file
        self.removeCurrentBestRoutes() #Truncate the current best routes files
        
        write_to_file = UnorderedList() #making it a linked list becaus its dynamically made
        write_to_file.add(["Origin","Dest1","Dest2","Dest3","Dest4","Home","Cost(Euro)","Aircraft"]) #header for output
        self.input_csv = inputCSV
         
        with open(self.input_csv) as csv_file:
            read_csv = csv.reader(csv_file, delimiter=',')  #takes each cell in the csv file
            for line in read_csv:
                                
                aircraft, cities = self.createVertices(line) #find the aircrafts and the different airports
                if aircraft == None and cities == None: # then go to the next route
                    print("=========================================================================================================================")
                    continue
                
                else:
                    cities_copy = cities[:] #copying the cities as they might be needed later
                    print("You have requested the best route for", cities, " using aircraft:", aircraft,"\n")
                    self.addVerticesToGraph(cities,directed_graph) # creating the cities of the graph
                    self.addEdgestoGraph(cities,directed_graph)  #adds the edges to the graph

                    path, total_cost = self.findShortestPath(directed_graph,cities,aircraft) # collect the return path and cost   
                    write_to_file.add(self.analyseBestJourney(path,total_cost,aircraft,cities_copy)) 
            
                
            self.writeToBestRoutesCsv(write_to_file) #writing the route to file 

        
        return ''

    
    def removeCurrentBestRoutes(self):
        
        '''this method truncates the bestRoutes csv that have previously been calculated '''
        #https://stackoverflow.com/questions/12277864/python-clear-csv-file
        #truncates the file if data already exists in it
        
        filename = "./data/BestRoutesGreedy.csv"
        f = open(filename, "w+") 
        f.close()
    
                
    def createVertices(self,line):
        
        ''' this method modifys the route by extracting the aircraft used and appending the starting 
        location to the end of the list '''
        
        self.route = line
        if len(self.route) == 5: #error handling. if there is no aircraft given then it just returns the route 
            if self.checkCitiesValid(self.route):
                return None,self.route
            else:
                print("There is an error in the inputed cities: ",self.route," and as a result we cannot calculate the best route")
                return None, None
        
        elif len(self.route) == 6: 
            self.aircraft = self.route[-1] #aircraft is the last element in the route.
            self.route = self.route[:-1] #route is everthing except the aircraft
            
            #checks to ensure that the aircraft and route entered are valid inputs(they exist in the created dictonaries)
            if self.checkAircraftValid(self.aircraft) and self.checkCitiesValid(self.route):
                return self.aircraft, self.route
            
            elif self.checkCitiesValid(self.route) and not self.checkAircraftValid(self.aircraft):
                print("The cities entered are valid, however the aircraft ",self.aircraft," is invalid. We will check for best route with no aircraft.\n")
                return None,self.route
            
            else:
                print("There is an error in the inputed cities: ",self.route," and as a result we cannot calculate the best route \n")
                return None,None
                        
        else:
            print("There is an error in the input. It does not input the correct number of airports and/or aircrafts")
            return None, None

    
        
    def checkAircraftValid(self,aircraft):
        
        ''' This function accepts an aircraft supplied by an itinery and checks that it is a valid aircraft'''
        
        #checking for a key in dictonary is o(1) because its hashed
        valid = False
        self.aircraft = aircraft
        
        if self.aircraft in self.aircraft_obj.aircraft_dict:
            valid = True
            
        return valid
        
        
    def checkCitiesValid(self,route):
        
        ''' This function accepts an route supplied and checks that it contains valid airports '''
        
        valid = False
        self.route = route
        
        for city in self.route:
            if city in self.atlas_obj.airport_dict:
                valid = True
            else:
                valid = False
                break
                 
        return valid
    
    
        
    def addVerticesToGraph(self,cities,graph):
        
        ''' This function accepts the different cities to be visited. It loops through them and creates 
        nodes in a graph. '''
        
        self.cities = cities
        for city in self.cities: 
            graph.add_vertex(city) #the cities are added to a set in the graph class

            
    
    def addEdgestoGraph(self,cities,graph):
        
        '''This function accepts the cities and a graph containing these cities and it adds links 
        between each city present in the graph with a weight of the cost of the trip'''
        
        self.cities = cities 
        for i in self.cities:
            for j in self.cities:
                if i != j: #this because dont need to link cities to themselves.

                    cost = self.atlas_obj.getCostOfTrip(i, j,self.currency_obj ,self.rate_obj) #cost of the trip is added as weight on the edges
                    graph.add_edge(i, j, cost) #adds the edges between nodes


                
    def findShortestPath(self,graph,cities,aircraft):
        
        ''' this function accepts the graph containing nodes and weighted edges between them, the list of cities to be 
         visted and the aircraft to be used in the itinery and finds the shortest path if possible'''
        
        self.cities = cities
        self.aircraft = aircraft
        current_city = self.cities[0] #this is the first city
        next_city_to_visit = current_city # setting this as a trap if no closest city is found
        original_start = current_city #original current_city needed for later on
        path = Queue() #Queue to store the best path
        path.enqueue(current_city) #adding the starting node to the best path 
        total_cost =0 # initalizing the total cost to 0
        self.cities.remove(current_city) #removing the starting point from the list of cities
    
        while len(self.cities) > 0 : #while there are still cities to be visited
            shortest_distance = 9999999999 
            
            for elem in self.cities: # for each remaining city in the list of cities
                distance = self.atlas_obj.getDistanceBetweenAirports(current_city,elem) #get the distance from the last city to this new one
                
                if self.aircraft != None: #if an aircraft is given
                    if graph.weights[current_city,elem] < shortest_distance and self.aircraft_obj.airplanePassFuel(distance,self.aircraft): #Check the distance is shorter and the aircraft can complete the journey
                            shortest_distance = graph.weights[current_city,elem] #new shortest distance    
                            next_city_to_visit = elem #next city to visit is this one
                          
                    else: #if its not shorter than the current shortest or it doesnt pass the fuel check then continue to next airport
                        continue
                else:
                    if graph.weights[current_city,elem] < shortest_distance: #Check the distance is shorter and the aircraft can complete the journey
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
                self.cities.remove(next_city_to_visit) #remove the city to be visited from the list of remaining cities
             
        # this will only be reached if the full path was made as it wouldve been returned earlier if not 
        last_stop = next_city_to_visit #the last city to visit before heading home
        path.enqueue(original_start) #add the original starting point to the queue 
        
        if self.aircraft != None:
            if (self.aircraft_obj.airplanePassFuel(self.atlas_obj.getDistanceBetweenAirports(last_stop,original_start),self.aircraft)): # check that the last stop to the starting point can be done
                total_cost += graph.weights[last_stop, original_start] # adding the cost the the toal cost 
                return path, total_cost #return the path and total cost
            
            else:
                return path, "cant complete trip" # if the plane cant complete the journey
        else:
            total_cost += graph.weights[last_stop, original_start] # adding the cost the the toal cost 
            return path, total_cost #return the path and total cost
    
    
    

    def analyseBestJourney(self,path,total_cost,aircraft,cities):
        
        ''' this method analyses the best path and its cost and prints appropiate messages
            it also returns the list to be wrtten to the bestRoutes csv'''
        
        route_to_file= [] 
        if path.size() == 6: #checking that the path is length of 6 otherwise the journey wasnt completed
            print("The best route is: ", end = ' ')
            
            while path.size() > 0: # loop until all finished
                city = path.dequeue() #remove the first element entered into the queue
                print(city, end= ' ') #print the dequeued element
                print('--->', end = ' ')
                route_to_file.append(city) #add the route to a list 
            print('Total cost is: €',total_cost) # print the cost
            route_to_file.append(total_cost)
            route_to_file.append(aircraft) # preparing to write list to file
            
        else:
            print("This journey cant be completed with the chosen aircraft")
            for city in cities:
                route_to_file.append(city)
            route_to_file.append(cities[0])
            route_to_file.append(total_cost)
            route_to_file.append(aircraft)
        print("=========================================================================================================================")
        
        return route_to_file
    
    
    
    def writeToBestRoutesCsv(self, write_to_file):
        
        '''this accepts a Queue of lists and writes them to a CSV'''
        
        with open('./data/BestRoutesGreedy.csv', "a") as csv_file:
            writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
            while write_to_file.size() != 0:
                last= write_to_file.returnLast()
                writer.writerow(last)
                write_to_file.remove(last)
                      
