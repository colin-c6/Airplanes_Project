import os
import csv
from functools import lru_cache

  
class Aircrafts():
    aircraft_dict = {}
      
    def __init__(self, airplanesFile):
        self.airplanesFile = airplanesFile
        self.aircraftDict(self.airplanesFile) #sends file to the aircraftDict function to create the dictonary 
        self.count = 0;
    
    
    @lru_cache(maxsize=2)
    def aircraftDict(self, airplaneFile):
        
        ''' This function creates a new aircraft dictonary 
            with all distances in metric units(km) '''
          
        self.airplaneFile = airplaneFile
        with open(os.path.join(self.airplaneFile),"rt", encoding="utf8" ) as airplaneFile: # r is for reading the file
            self.airplane_csv_reader = csv.reader(airplaneFile)
            for column in self.airplane_csv_reader:

                distance_in_km = self.metricsConversion(column[2],column[4]) #send the type and distance to the converter
                self.aircraft_dict[column[0]] = distance_in_km 
        
        #for i in self.aircraft_dict:
            #print (i,self.aircraft_dict[i]) prints out the contents of the dictonary
        return
    
    def metricsConversion(self,value_type,distance):
        
        ''' This funtion takes in the metric value and current distance and if 
            distance is in imperial format(miles) it converts it to metric(km) '''
       
        self.value_type = value_type
        self.distance = distance
        
        if (self.value_type== "imperial"):
            self.distance = int(self.distance)
            return self.distance *1.60934
        
        else:
            return self.distance
        
        
    def airplanePassFuel(self,dis,aircraft):
        
        ''' This function checks whether the aircraft passes the fuel check '''
        self.dis = dis
        self.aircraft = aircraft
        #self.aircraft_obj = aircraft_obj
        
        #print("Printing distance to be checked: ", self.dis)
        #print("Printing the aircraft: ", self.aircraft)
        #print("Printing capacity of the aircraft: ",self.aircraft_dict[self.aircraft])
        self.count +=1
        #print("count",self.count)
        #print("------------------------------------")
        
        var=False
        for x in self.dis:
            if x > int(self.aircraft_dict[self.aircraft]):
                var =False
                break
                
            else:
                var = True
        
        return var