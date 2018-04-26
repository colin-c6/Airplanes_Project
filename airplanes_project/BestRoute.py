import csv
import itertools
from data_structures import Graph, Queue

class Itinerary():
    
    ''' This class finds the all the possible routes in an itinery, prices them 
    checks that plane has enough fuel capacity and returns the best route. '''
    
    def __init__(self,aircraftPass, atlasObj):
        
        ''' this method initalized an instance of the Itinerary class '''
        
        self.aircraftPass = aircraftPass
        self.atlasObj = atlasObj
        
    
    def findBestRoute(self, inputCSV):
        
        ''' This method is the centralhub of the bestRoute file and it drives 
        the methods that find the best route and then writes them to a file '''
        graph = Graph() #creating instance of graph that will be used to make directed graph

        #https://stackoverflow.com/questions/12277864/python-clear-csv-file
        #truncates the file if data already exists in it
        filename = "./data/BestRoutes.csv"
        f = open(filename, "w+") 
        f.close()
        
        writeToFileList = [["Origin","Dest1","Dest2","Dest3","Dest4","Home","Cost"]] #header for output
        self.inputSet = [] #needs to be a list because aircraft is included
        self.inputCSV = inputCSV
        
        with open(self.inputCSV) as csvfile:  
            readCSV = csv.reader(csvfile, delimiter=',')  #takes each cell in the csv file and stores in list
            for line in readCSV:
                self.inputSet = line 
            
                aircraft, modified_route = self.modifyingRoute(self.inputSet) #finding the aircraft if it exsists and the complete route
                self.make_graph(modified_route,graph) #make the graph with the cities
                
                #If there is no airport specified in a csv
                if len(aircraft) == 0:
                    print("You have requested the best route for: ", modified_route, " with no specified aircraft ","\n")
                    allPossibleRoutes = self.allPossibleRoutesTaken(modified_route)
                    best_journey = self.distCostOfAllJourneys(allPossibleRoutes,graph)
                    aircraft= "with no aircraft specified this route"
                
                # this is activated if there is an airport present
                else:
                    print("You have requested the best route for: ", modified_route, " with aircraft: ", aircraft,"\n")
                    allPossibleRoutes = self.allPossibleRoutesTaken(modified_route) #finding all the possible routes
                    best_journey = self.distCostOfAllJourneysAircraft(aircraft,allPossibleRoutes,graph) #find the best journey


                #if there is no possible journey 
                if len(best_journey) == 0:
                    print(aircraft, "is unable to complete journey \n")
                    print("=============================================================================================================================")
                    continue
                 
                else:  
                    print(aircraft ," meets all specifications and the best route to take is: ", best_journey[0], "and the cost is:    €",best_journey[1],"\n")
                    print("=============================================================================================================================")
                    final_itinery = best_journey[0]
                    final_itinery.append(best_journey[1])
                    writeToFileList.append(final_itinery)  
                          
   
            with open('./data/BestRoutes.csv', "a") as csv_file:
                writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
                for line in writeToFileList:
                    writer.writerow(line)
                        #https://stackoverflow.com/questions/2084069/create-a-csv-file-with-values-from-a-python-list
        
    
    
    def modifyingRoute(self, route):
        
        ''' this method modifys the route by extracting the aircraft used and appending the starting 
        location to the end of the list '''
        
        self.route = route
        if len(self.route) == 5: #error handling. if there is no aircraft given then it just returns the route 
            return '',self.route
        
        elif len(self.route) == 6:
            self.aircraft = self.route[-1] #aircraft is the last element in the route. 
            self.route = self.route[:-1]
            return self.aircraft, self.route
        else:
            print("There is an error in the input. It does not input the correct number of airports and/or aircrafts")
        
    
    
    def make_graph(self,cities,graph):
        
        ''' this method creates a directional weighted graph. the Cities are the nodes, they are connected by edges and 
        these edges weights is equal to the cost of the journey '''
        
        self.cities = cities 
        for x in self.cities:
            graph.add_vertex(x) #adds the nodes to the graph (in a set)
        
        for i in self.cities: 
            for j in self.cities:
                if i != j:

                    cost = self.atlasObj.getCostOfTrip(i, j)
                    graph.add_edge(i, j, cost) #creates the weighted edges between the graphs based on the cost of going betwen them

        return ''


    
    def allPossibleRoutesTaken(self, modifRoutes):
         
        ''' this method accepts a modified route calculates all the possible permutations
        for the route  source: https://docs.python.org/2/library/itertools.html'''
         
        self.modifRoutes = modifRoutes
        possibleRoutes = list(itertools.permutations(self.modifRoutes[1:])) #possible routes is an array of tuples needed to convert these to lists    
        possibleRoutesConvert=[]                                            # for manipulation        
        for x in possibleRoutes:
            possibleRoutesConvert.append(list(x)) #the middle 4 cities are now stored in a list
      
        # adding the start and finish airport to allPossibleRoutes
        startFinishAirport = [self.modifRoutes[0],]
        allPossibleRoutes = Queue() #creating a queue to store the possible combinations.
        for possRoute in possibleRoutesConvert:
            allPossibleRoutes.enqueue(tuple(startFinishAirport +possRoute+ startFinishAirport)) #adding the start and end airport to each possibility
                                                                                                # and placing in a queue
        return allPossibleRoutes


    def distCostOfAllJourneys(self, possibleRoutes,graph):
         
        ''' This method accepts the aircraft, a graph and all the possible routes in an intinery. It checks that a route can be completed given
        the aircraft and if it can, it calculates the total cost of the journey and finally returns the cheapest journey'''
        
        self.possibleRoutes = possibleRoutes #this is a queue
        self.graph_costs = graph.weights #

        min_cost = 9999999999999999 #default
        best_cost = []

        while self.possibleRoutes.size() != 0: #while the queue isnt empty
            total_cost = 0 # default for total cost is 0
            route = self.possibleRoutes.dequeue() #take a route
             
            for k in range (0,len(route)-1,1): # need to use -1 because im using k+1   
                total_cost += self.graph_costs[(route[k], route[k+1])] #add the total cost of the journey from the graph created earlier
                    
            if total_cost < min_cost: #check that its cheaper than the current cheapest
                best_cost.clear() #remove whats in the list
                best_cost.append(list(route)) #add the best route
                best_cost.append(total_cost) #add the cost of the best route 
                min_cost = total_cost # update the minimum cost

        return best_cost #return the best route
    
    
    
    
         
    def distCostOfAllJourneysAircraft(self,aircraft, possibleRoutes,graph):
         
        ''' This method accepts the aircraft, a graph and all the possible routes in an intinery. It checks that a route can be completed given
        the aircraft and if it can, it calculates the total cost of the journey and finally returns the cheapest journey'''
        
        self.aircraft= aircraft
        print("Please wait while we check that aircraft ",self.aircraft," meets the required specifications.\n") 
        self.possibleRoutes = possibleRoutes #this is a queue
        self.graph_costs = graph.weights #

        min_cost = 9999999999999999 #default
        best_cost = []

        while self.possibleRoutes.size() != 0: #while the queue isnt empty
            total_cost = 0 # default for total cost is 0
            route = self.possibleRoutes.dequeue() #take a route
             
            for k in range (0,len(route)-1,1): # need to use -1 because im using k+1   
                distance = self.atlasObj.getDistanceBetweenAirports(route[k], route[k+1]) #get distance of first two cities in route
                if not (self.aircraftPass.airplanePassFuel(distance,self.aircraft)): #check that the aircraft can fly that distance
                    break # if it cant then move to another route 
                else:
                    total_cost += self.graph_costs[(route[k], route[k+1])] #add the total cost of the journey from the graph created earlier
                    
            if total_cost < min_cost: #check that its cheaper than the current cheapest
                best_cost.clear() #remove whats in the list
                best_cost.append(list(route)) #add the best route
                best_cost.append(total_cost) #add the cost of the best route 
                min_cost = total_cost # update the minimum cost

        return best_cost #return the best route
    
    