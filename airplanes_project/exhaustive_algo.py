import csv
import itertools
from data_structures import Graph, Queue, UnorderedList


class Itinerary():
    
    ''' This class finds the all the possible routes in an itinery, prices them 
    checks that plane has enough fuel capacity and returns the best route. '''
    
    def __init__(self,aircraft, atlas ,currency ,rate):
        
        ''' this method initalized an instance of the Itinerary class '''
        
        self.aircraft_obj = aircraft
        self.atlas_obj = atlas
        self.currency_obj = currency
        self.rate_obj = rate

   
        
    
    def findBestRoute(self, inputCSV):
        
        ''' This method is the centralhub of the bestRoute file and it drives 
        the methods that find the best route and then writes them to a file '''
        
        graph = Graph() #creating instance of graph that will be used to make directed graph
        self.removeCurrentBestRoutes() #Truncate the current best routes files

        write_to_file = UnorderedList() #making it a linked list becaus its dynamically made
        write_to_file.add(["Origin","Dest1","Dest2","Dest3","Dest4","Home","Cost(Euro)","Aircraft"]) #header for output
        
        self.inputCSV = inputCSV
        route_count = 1
        
        with open(self.inputCSV) as csvfile:  
            read_csv = csv.reader(csvfile, delimiter=',')  #takes each cell in the csv file and stores in list
            
            for line in read_csv:
                print("Route number: ",route_count)
                
                aircraft, modified_route = self.modifyingRoute(line) #finding the aircraft if it exsists and the complete route
                if aircraft == None and modified_route == None:
                    print("==================================================================================================================================")
                    route_count+=1
                    continue
    
                else:
                    self.make_graph(modified_route,graph) #make the graph with the cities
                    #If there is no airport specified in a csv
                    
                    if aircraft == None:
                        print("You have requested the best route for: ", modified_route, " with no specified aircraft ","\n")
                        all_possible_routes = self.allPossibleRoutesTaken(modified_route)
                        best_journey = self.distCostOfAllJourneys(all_possible_routes,graph)
                        aircraft= "no aircraft specified"
                    
                    # this is activated if there is an airport present
                    else:
                        print("You have requested the best route for: ", modified_route, " with aircraft: ", aircraft,"\n")
                        all_possible_routes = self.allPossibleRoutesTaken(modified_route) #finding all the possible routes
                        best_journey = self.distCostOfAllJourneysWithAircraft(aircraft,all_possible_routes,graph) #find the best journey
                    
                    write_to_file.add(self.analyseBestJourney(best_journey,aircraft,modified_route)) 
                              
                self.writeToBestRoutesCsv(write_to_file)
                route_count+=1
                
                
        return ''
        
    def make_graph(self,cities,graph):
        
        ''' this method creates a directional weighted graph. the Cities are the nodes, they are connected by edges and 
        these edges weights is equal to the cost of the journey '''
        
        self.cities = cities 
        for city in self.cities:
            graph.add_vertex(city) #adds the nodes to the graph (in a set)
        
        for city1 in self.cities: 
            for city2 in self.cities:
                if city1 != city2:

                    cost = self.atlas_obj.getCostOfTrip(city1, city2,self.currency_obj ,self.rate_obj)
                    graph.add_edge(city1, city2, cost) #creates the weighted edges between the graphs based on the cost of going betwen them

        return graph
    
    def removeCurrentBestRoutes(self):
        
        '''this method truncates the bestRoutes csv that have been calculated '''
        #https://stackoverflow.com/questions/12277864/python-clear-csv-file
        #truncates the file if data already exists in it
        
        filename = "./data/BestRoutes.csv"
        f = open(filename, "w+") 
        f.close()
    
        
    def modifyingRoute(self, route):
        
        ''' this method modifys the route by extracting the aircraft used and appending the starting 
        location to the end of the list '''
        
        self.route = route
        if len(self.route) == 5: #error handling. if there is no aircraft given then it just returns the route 
            if self.checkCitiesValid(self.route):
                return None,self.route
            else:
                print("There is an error in the inputed cities: ",self.route," and as a result we cannot calculate the best route")
                return None, None
            
        elif len(self.route) == 6:
            
            self.aircraft = self.route[-1] #aircraft is the last element in the route.
            self.route = self.route[:-1]
            
            #checks to ensure that the aircraft and route entered are valid inputs(they exist in the created dictonaries)
            if self.checkAircraftValid(self.aircraft) and self.checkCitiesValid(self.route):
                return self.aircraft, self.route
            
            elif self.checkCitiesValid(self.route) and not self.checkAircraftValid(self.aircraft):
                print("The cities entered are valid, however the aircraft ",self.aircraft," is invalid. We will check for best route with no aircraft.\n")
                return None,self.route
            
            else:
                print("There is an error in the inputed cities: ",self.route," and as a result we cannot calculate the best route")
                return None,None
                        
        else:
            print("There is an error in the input. It does not input the correct number of airports and/or aircrafts \n")
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
    
    def allPossibleRoutesTaken(self, modifRoutes):
         
        ''' this method accepts a modified route calculates all the possible permutations
        for the route  source: https://docs.python.org/2/library/itertools.html'''
         
        self.modifed_routes = modifRoutes
        possible_routes = list(itertools.permutations(self.modifed_routes[1:])) #possible routes is an array of tuples needed to convert these to lists    
        possible_routes_convert=[]                                            # for manipulation        
        for x in possible_routes:
            possible_routes_convert.append(list(x)) #the middle 4 cities are now stored in a list
      
        # adding the start and finish airport to all_possible_routes
        start_finish_airport = [self.modifed_routes[0],]
        all_possible_routes = Queue() #creating a queue(linked-list) to store the possible combinations.
        for possRoute in possible_routes_convert:
            all_possible_routes.enqueue(tuple(start_finish_airport +possRoute+ start_finish_airport)) #adding the start and end airport to each possibility
                                                                                                # and placing in a queue. Adding as tuple as I dont 
        return all_possible_routes                                                                # any modification to be able to occur



    def distCostOfAllJourneys(self, possible_routes,graph):
         
        ''' This method accepts a graph and all the possible routes in an intinery. 
            It calculates the total cost of the journey and finally returns the cheapest journey'''
        
        self.possible_routes = possible_routes #this is a queue
        self.graph_costs = graph.weights #

        min_cost = 9999999999999999 #default
        best_cost = []

        while self.possible_routes.size() != 0: #while the queue isnt empty
            total_cost = 0 # default for total cost is 0
            route = self.possible_routes.dequeue() #take a route
             
            for k in range (0,len(route)-1,1): # need to use -1 because im using k+1   
                total_cost += self.graph_costs[(route[k], route[k+1])] #add the total cost of the journey from the graph created earlier
                    
            if total_cost < min_cost: #check that its cheaper than the current cheapest
                best_cost.clear() #remove whats in the list
                best_cost.append(list(route)) #add the best route
                best_cost.append(total_cost) #add the cost of the best route 
                min_cost = total_cost # update the minimum cost

        return best_cost #return the best route
    
    
    
    
         
    def distCostOfAllJourneysWithAircraft(self,aircraft, possible_routes,graph):
         
        ''' This method accepts the aircraft, a graph and all the possible routes in an intinery. It checks that a route can be completed given
        the aircraft and if it can, it calculates the total cost of the journey and finally returns the cheapest journey'''
        
        self.aircraft= aircraft
        print("Please wait while we check that aircraft ",self.aircraft," meets the required specifications.\n") 
        self.possible_routes = possible_routes #this is a queue
        self.graph_costs = graph.weights 

        min_cost = 9999999999999999 #default
        best_cost = []

        while self.possible_routes.size() != 0: #while the queue isnt empty
            aircraftPass = True
            total_cost = 0 # default for total cost of a route is 0
            route = self.possible_routes.dequeue() #take a route from the queue
            for k in range (0,len(route)-1,1): # need to use -1 because im using k+1   
                
                distance = self.atlas_obj.getDistanceBetweenAirports(route[k], route[k+1]) #get distance of two cities in route
                if not (self.aircraft_obj.airplanePassFuel(distance,self.aircraft)): #check that the aircraft can fly that distance
                    aircraftPass = False
                    break # if it cant then move to another route 
                else:
                    total_cost += self.graph_costs[(route[k], route[k+1])] #add the total cost of the journey from the graph created earlier
            
            if (aircraftPass):
                if total_cost < min_cost and total_cost > 0: #check that its cheaper than the current cheapest
                    best_cost.clear() #remove whats in the list
                    best_cost.append(list(route)) #add the best route --> O(1) because i have emptied the list
                    best_cost.append(total_cost) #add the cost of the best route 
                    min_cost = total_cost # update the minimum cost

        return best_cost #return the best route
    
    
    def analyseBestJourney(self,best_journey,aircraft,modified_route):
        
        if len(best_journey) == 0:
            print(aircraft, "is unable to complete journey \n")
            print("=============================================================================================================================")
            final_itinery = modified_route
            final_itinery.append(str(modified_route[0]))
            final_itinery.append("N/A")
            final_itinery.append("Not Feasible")
            return final_itinery
                     
        else:  
            print(aircraft ," meets all specifications and the best route to take is: ", best_journey[0], "and the cost is:    €",best_journey[1],"\n")
            print("=============================================================================================================================")
            final_itinery = best_journey[0]
            final_itinery.append(best_journey[1])
            final_itinery.append(aircraft)
            return final_itinery
                      
        
    def writeToBestRoutesCsv(self, write_to_file):
        
        '''this accepts a list of lists and writes them to a CSV'''
        
        with open('./data/BestRoutes.csv', "a") as csv_file:
            writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
            while write_to_file.size() != 0:
                last= write_to_file.returnLast()
                writer.writerow(last)
                write_to_file.remove(last)
                 
            #https://stackoverflow.com/questions/2084069/create-a-csv-file-with-values-from-a-python-list
    