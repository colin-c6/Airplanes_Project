import os
import csv
from functools import lru_cache

  
class Aircrafts():
    aircraft_dict = {}
      
    def __init__(self, airplanes_file):
        self.airplanes_file = airplanes_file
        self.aircraftDict(self.airplanes_file) #sends file to the aircraftDict function to create the dictonary 
    
    
    @lru_cache(maxsize=2)
    def aircraftDict(self, airplanes_file):
        
        ''' This function creates a new aircraft dictonary 
            with all distances in metric units(km) '''
          
        self.airplanes_file = airplanes_file
        with open(os.path.join(self.airplanes_file),"rt", encoding="utf8" ) as airplanes_file: # r is for reading the file
            self.airplane_csv_reader = csv.reader(airplanes_file)
            for column in self.airplane_csv_reader:

                distance_in_km = self.metricsConversion(column[2],column[4]) #send the type and distance to the converter
                self.aircraft_dict[column[0]] = distance_in_km #airplane is now asociated with a distance in a dictonary
        
        return
    
    def metricsConversion(self,value_type,distance):
        
        ''' This function takes in the metric value and current distance and if 
            distance is in imperial format(miles) it converts it to metric(km) '''
       
        self.value_type = value_type
        self.distance = distance
        
        if (self.value_type== "imperial"): #if the plane max distance is in imperial then convert it 
            self.distance = float(self.distance)
            return self.distance *1.60934
        
        else:
            return self.distance
        
        
    def airplanePassFuel(self,distance,aircraft):
        
        ''' This function checks whether the aircraft passes the fuel check. Can accept single distances of lists '''
        self.distance = distance
        self.aircraft = aircraft

        var = False
        #this part is for greedy algorithm part
        if isinstance(self.distance,int) or isinstance(self.distance, float): #check that the distance is a float or int
            if self.distance > int(self.aircraft_dict[self.aircraft]): #if the distance is greater than the planes capacity 
                    var =False
            else:
                    var = True #if the plane is capable of flying the journey
      
            return var
        
        
        #this part is used for brute force soltuion (accepts a list)
        else:
            for distance in self.distance: # for each distance in the distances
                if distance > int(self.aircraft_dict[self.aircraft]): #if the distance is greater than the plan capacity return false
                    var =False
                    break    
                else:
                    var = True
            
            return var