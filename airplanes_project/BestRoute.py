
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
        
        writeToFileList = [["Origin","Dest1","Dest2","Dest3","Dest4","Home","Cost"]]
        self.inputSet = set()
        self.inputCSV = inputCSV
        
        with open(self.inputCSV) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            
            for line in readCSV:
                self.inputSet = line # i think this changes it back to a list. have a look
            
                aircraft, modified_route = self.modifyingRoute(self.inputSet) 
                #distanceOfModifiedRoute, costOfModifiedRoute = self.costOfSingleRoute(modified_route) #gets the cost of the single trip. useless really
                allPossibleRoutes = self.allPossibleRoutesTaken(modified_route)
                distanceAllJourneys, costAllJourneys = self.distCostOfAllJourneys(aircraft,allPossibleRoutes)
                if len(distanceAllJourneys) == 0:
                    print(aircraft, "is unable to complete journey")
                    print("=============================================================================================================================")
                    print("=============================================================================================================================")
                    
                    continue
                else:
                
                
                    costOfEachPossibleRoute = self.allRouteCosts(costAllJourneys)
                    bestRouteByCost, bestRouteByIndex = self.bestRoute(costOfEachPossibleRoute)
                    
                    print("The best route to take is: ", allPossibleRoutes[bestRouteByIndex[0]], "and the cost is: ", bestRouteByCost[0])
                    print("=============================================================================================================================")
                  
                    routeCostList = allPossibleRoutes[bestRouteByIndex[0]]
                    routeCostList.append(bestRouteByCost[0])
                    writeToFileList.append(routeCostList)
                            
            with open('BestRoutes.csv', "a") as csv_file:
                        writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
                        for line in writeToFileList:
                            writer.writerow(line)
                        #https://stackoverflow.com/questions/2084069/create-a-csv-file-with-values-from-a-python-list
                    
                    
            
                #return self.inputSet #this is the first route of the data 
        
    
    
    def modifyingRoute(self, route):
        
        ''' this method modifys the route by extracting the aircraft used and appending the starting 
        location to the end of the list '''
        
        #print(type(route))
        self.route = route
        self.aircraft = self.route[-1] #aircraft is the last element in the route. may need to change because this is optional 
        self.route = self.route[:-1]  # removing the aircraft from the route  
        self.route.append(route[0]) #appending the starting point to the end of the route
        #print("modified route(removed aircraft and added start point to end: ",self.route)
    
        return self.aircraft, self.route
        
    
    
    def costOfSingleRoute(self,modRoute):
        
        #this method isnt implemented at the minute. its not needed
        '''Method to calculate the cost of a single route in an itinery
        it adds these costs to a list  '''
        
        self.modRoute = modRoute
        
        distances= [] #list to hold all the distances
        costs = [] # list to hold cost of each route 
        for i in  range (0,len(self.modRoute)-1,1): #using -1 or will go out of range of the list
            distances.append(self.atlasObj.getDistanceBetweenAirports(self.modRoute[i], self.modRoute[i+1]))
            costs.append(self.atlasObj.getCostOfTrip(self.modRoute[i], self.modRoute[i+1]))
            
            #print(self.modRoute[i], self.modRoute[i+1])
            #print(distances)
            #print(costs)
        return distances, costs
        
        
    
    def allPossibleRoutesTaken(self, modifRoutes):
        
        ''' this method accepts a modified route with the last stop the 
        same as the starting point and calculates all the possible combinations
        for the route  '''
        
        self.modifRoutes = modifRoutes
        possibleRoutes = list(itertools.permutations(self.modifRoutes[1:-1]))
        # The permeautatiosn method result in tuples embedded in a list. needed to convert these to lists    
        possibleRoutesConvert=[]
        for x in possibleRoutes:
            possibleRoutesConvert.append(list(x))
    
    
    
        # adding the start and finish airport to allPossibleRoutes
        startFinishAirport = [self.modifRoutes[0],]
        allPossibleRoutes = []
        for possRoute in possibleRoutesConvert:
            allPossibleRoutes.append(startFinishAirport +possRoute+ startFinishAirport)
            
        print("Printing all the possibly routes: ")
        print(allPossibleRoutes)
        print("Printing number of possible routes: ")
        print(len(allPossibleRoutes))
        print("------------------------------------")
        return allPossibleRoutes
        
        
        
    def distCostOfAllJourneys(self,aircraft, possibleRoutes):
        
        ''' This method accepts the aircraft and all the possible routes in an intinery. It calculates the distance of each 
        journey in an itineary. It then checks that its possible for the aircraft to complete the journey. Finally it
        only returns routes that can be completed, along with their costs. '''
        
        self.aircraft= aircraft
        self.possibleRoutes = possibleRoutes
        #Getting all the distances for each individual journey in a possible route and their corresponding costs    
        all_distances= []
        all_costs = []
        for j in  range (0,len(self.possibleRoutes),1):
            print("checking route: ", self.possibleRoutes[j])
            indiviualDistances= []
            individualCosts=[]
            for k in  range (0,len(self.possibleRoutes[0])-1,1): # need to use -1 because im using k+1
                
                indiviualDistances.append(self.atlasObj.getDistanceBetweenAirports(self.possibleRoutes[j][k], self.possibleRoutes[j][k+1]))
                individualCosts.append(self.atlasObj.getCostOfTrip(self.possibleRoutes[j][k], self.possibleRoutes[j][k+1]))
                #print("after return indiviusal distnce is :", indiviualDistances)

            if(self.aircraftPass.airplanePassFuel(indiviualDistances,self.aircraft)):
            
                all_distances.append(indiviualDistances)
                all_costs.append(individualCosts)
        

        print("Printing all the distances: ")
        print(all_distances)
        print("------------------------------------")
        
        print("Printing cost of all the distances: ")
        print(all_costs)
        print("------------------------------------")
        
        return all_distances, all_costs
        
  
    
    
    def allRouteCosts(self, routeLegsCost):
        
        ''' this method adds the cost of each leg of an itinerary and returns the total cost in a list'''
        
        self.routeLegsCost = routeLegsCost
        
        total_cost=[]
        for n in  range (0,len(self.routeLegsCost),1): 
            total=0
            for m in range (0,len(self.routeLegsCost[0]),1):
                total += self.routeLegsCost[n][m]
            total_cost.append(total)
            
        print("Printing cost in total for each itinery: ")
        print(total_cost)
        print("------------------------------------")
        return total_cost        
        
    
    def bestRoute(self,costOfEachRoute):
        
        ''' this method returns sorted cost of each itinery and the index of it'''
        
        self.costOfEachRoute = costOfEachRoute
        sortedTotalCosts = sorted(self.costOfEachRoute) 
        sortedCostsIndex = sorted(range(len(self.costOfEachRoute)), key=lambda k: self.costOfEachRoute[k]) #sorted array by index
        
        print("Printing sorted cost in total for each itinery: ")
        print(sortedTotalCosts)
        print()
        print("sorting the costs in total by index: ")
        print(sortedCostsIndex)
        print("------------------------------------")
        
        return sortedTotalCosts, sortedCostsIndex
