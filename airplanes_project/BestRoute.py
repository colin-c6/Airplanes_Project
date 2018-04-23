import collections
import math 
import csv
import itertools

class Itinerary():
    
    ''' This class finds the all the possible routes in an itinery, prices them 
    checks that plane has enough fuel capacity and returns the best route. '''
    
    def __init__(self,aircraftPass, atlasObj):
        
        ''' this method initalized an instance of the Itinerary class '''
        
        self.aircraftPass = aircraftPass
        self.atlasObj = atlasObj
        self.count = 0
        
    
    def findBestRoute(self, inputCSV):
        
        ''' This method is the centralhub of the bestRoute file and it drives 
        the methods that find the best route and then writes them to a file '''
        graph = Graph()
        
        writeToFileList = [["Origin","Dest1","Dest2","Dest3","Dest4","Home","Cost"]]
        self.inputSet = set()
        self.inputCSV = inputCSV
        
        with open(self.inputCSV) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',') 
            for line in readCSV:
                self.inputSet = line # i think this changes it back to a list. have a look
            
                aircraft, modified_route = self.modifyingRoute(self.inputSet)
                print("You have requested the best route for: ", modified_route, " with aircraft: ", aircraft,"\n")
                self.make_graph(modified_route,graph)

                allPossibleRoutes = self.allPossibleRoutesTaken(modified_route)
                distanceAllJourneys, costAllJourneys = self.distCostOfAllJourneys(aircraft,allPossibleRoutes,graph)
                if len(distanceAllJourneys) == 0:
                    print(aircraft, "is unable to complete journey \n")
                    print("=============================================================================================================================")
                    continue
                
                else:
                    costOfEachPossibleRoute = self.allRouteCosts(costAllJourneys)
                    bestRouteByCost, bestRouteByIndex = self.bestRoute(costOfEachPossibleRoute)
                     
                    print(aircraft ," has met all specifications and the best route to take is: ", allPossibleRoutes[bestRouteByIndex[0]], "and the cost is: ", bestRouteByCost[0],"\n")
                    print("=============================================================================================================================")
                   
                    routeCostList = allPossibleRoutes[bestRouteByIndex[0]]
                    routeCostList.append(bestRouteByCost[0])
                    writeToFileList.append(routeCostList)
                             
            with open('BestRoutes.csv', "a") as csv_file:
                        writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
                        for line in writeToFileList:
                            writer.writerow(line)
                        #https://stackoverflow.com/questions/2084069/create-a-csv-file-with-values-from-a-python-list
        return ''
    
    
    def modifyingRoute(self, route):
        
        ''' this method modifys the route by extracting the aircraft used and appending the starting 
        location to the end of the list '''
        
        #print(type(route))
        self.route = route
        self.aircraft = self.route[-1] #aircraft is the last element in the route. may need to change because this is optional 
        self.route = self.route[:-1]
    
        return self.aircraft, self.route
        
    
    
    def make_graph(self,cities,graph):
        
        ''' this method creates a directional weighted graph. the Cities are the nodes, they are connected by edges and 
        these edges weights is equal to the cost of the journey '''
        
        self.cities = cities
        for x in self.cities:
            graph.add_vertex(x)
        
        for i in self.cities:
            for j in self.cities:
                if i != j:

                    cost = self.atlasObj.getCostOfTrip(i, j)
                    graph.add_edge(i, j, cost)

        return ''


    
    def allPossibleRoutesTaken(self, modifRoutes):
         
        ''' this method accepts a modified route with the last stop the 
        same as the starting point and calculates all the possible combinations
        for the route  '''
         
        self.modifRoutes = modifRoutes
        possibleRoutes = list(itertools.permutations(self.modifRoutes[1:]))
        # The permeautatiosn method result in tuples embedded in a list. needed to convert these to lists    
        possibleRoutesConvert=[]
        for x in possibleRoutes:
            possibleRoutesConvert.append(list(x))
     
        # adding the start and finish airport to allPossibleRoutes
        startFinishAirport = [self.modifRoutes[0],]
        allPossibleRoutes = []
        for possRoute in possibleRoutesConvert:
            allPossibleRoutes.append(startFinishAirport +possRoute+ startFinishAirport)
             
        #print("Printing all the possibly routes: ")
        #print(allPossibleRoutes)
        #print("------------------------------------")
        return allPossibleRoutes
#         
#         
#         
    def distCostOfAllJourneys(self,aircraft, possibleRoutes,graph):
         
        ''' This method accepts the aircraft and all the possible routes in an intinery. It calculates the distance of each 
        journey in an itineary. It then checks that its possible for the aircraft to complete the journey. Finally it
        only returns routes that can be completed, along with their costs. '''
        
        self.aircraft= aircraft
        print("Please wait while we check that aircraft ",self.aircraft," meets the required specifications.\n") 
        self.possibleRoutes = possibleRoutes
        self.graph_costs = graph.weights
        
        #Getting all the distances for each individual journey in a possible route and their corresponding costs    
        all_distances= []
        all_costs = []
        for j in range (0,len(self.possibleRoutes),1):
            #print(self.possibleRoutes[j])
            indiviualDistances= []
            individualCosts=[]
            
            for k in  range (0,len(self.possibleRoutes[0])-1,1): # need to use -1 because im using k+1     
                indiviualDistances.append(self.atlasObj.getDistanceBetweenAirports(self.possibleRoutes[j][k], self.possibleRoutes[j][k+1]))
                individualCosts.append(self.graph_costs[(self.possibleRoutes[j][k], self.possibleRoutes[j][k+1])])
 
            if(self.aircraftPass.airplanePassFuel(indiviualDistances,self.aircraft)):
                all_distances.append(indiviualDistances)
                all_costs.append(individualCosts)
         
        #print("Printing all the distances: ")
        #print(all_distances)
        #print("------------------------------------")
         
        #print("Printing cost of all the distances: ")
        #print(all_costs)
        #print("------------------------------------")
         
        return all_distances, all_costs
         
#   
#     
#     
    def allRouteCosts(self, routeLegsCost):
         
        ''' this method adds the cost of each leg of an itinerary and returns the total cost in a list'''
         
        self.routeLegsCost = routeLegsCost  
        total_cost=[]
        for n in  range (0,len(self.routeLegsCost),1): 
            total=0
            for m in range (0,len(self.routeLegsCost[0]),1):
                total += self.routeLegsCost[n][m]
            total_cost.append(total)
             
        #print("Printing cost in total for each itinery: ")
        #print(total_cost)
        #print("------------------------------------")
        return total_cost        
         
     
    def bestRoute(self,costOfEachRoute):
         
        ''' this method returns sorted cost of each itinery and the index of it'''
         
        self.costOfEachRoute = costOfEachRoute
        sortedTotalCosts = sorted(self.costOfEachRoute) 
        sortedCostsIndex = sorted(range(len(self.costOfEachRoute)), key=lambda k: self.costOfEachRoute[k]) #sorted array by index
         
        #print("Printing sorted cost in total for each itinery: ")
        #print(sortedTotalCosts)
        #print()
        #print("sorting the costs in total by index: ")
        #print(sortedCostsIndex)
        #print("------------------------------------")
         
        return sortedTotalCosts, sortedCostsIndex

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

