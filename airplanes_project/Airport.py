
'''
Created on 22 Mar 2018

@author: colin
'''
import os
import csv
from math import pi, sin, cos, acos 
from functools import lru_cache

class Airport():
    '''
    class to generates objects of airports
    '''

    def __init__(self,country, code, latitude, longitude ):
        '''
        Airport Constructor that initializes Airport objects
        '''
        self.country = country
        self.code = code
        self.latitude = latitude
        self.longitude = longitude
        
        

class AirportAtlas():
    
    ''' Controls the airport atlas and contains methods to find cost and distance of routes '''
    
    airport_dict = {} # initalising an empty dictonary for the airport atlas
    def __init__(self,csv_file):
        
        ''' Initsalizing method reads in the airports csv file, and creates the airport, 
        currency and curreny rate dictonaries '''
                
        self.csv_airport_file = csv_file
        self.createAirportDict(self.csv_airport_file)
        
         
    
    @lru_cache(maxsize=2)
    def createAirportDict(self, csv_file):
        
        ''' Method to create the Airport Dictionary. uses the 3 letter airport code and
        creates airport objects '''
        
        self.csv_file = csv_file
        with open(os.path.join(self.csv_file),"rt", encoding="utf8" ) as csv_file: # r is for reading the file
            self.csv_reader = csv.reader(csv_file) # reader expects values to be seperated by a commma.
                                        # need to iterate over csv_reader at present its just an object in memory
            self.airport_dict = {column[4] : Airport(column[3],column[4],column[6],column[7]) for column in self.csv_reader}
            #create the airport dictonary
                    
        return self.airport_dict

       
    def getAirport(self,code): 
        
        ''' When invoked with a 3 letter code, this method returns the corresponding airport 
        from the airport dictonary '''
        
        self.code = code
        return (self.airport_dict[self.code])
    

    @staticmethod
    def greatCircledList(lat1, long1, lat2, long2):
        
        '''Method to find the distance between two points given the latitudes and longitudes of those points'''
        
        radius_earth = 6371
        theta1 = float(long1) * (2 * pi) / 360
        theta2 = float(long2) * (2 * pi) / 360
        phi1 = (90 - float(lat1)) * (2 * pi) / 360
        phi2 = (90 - float(lat2)) * (2 * pi) / 360
        distance = acos(sin(phi1) * sin(phi2) * cos(theta1 - theta2) + cos(phi1) * cos(phi2)) * radius_earth
        distance = distance
        return distance
    
    
    def getDistanceBetweenAirports(self, code1, code2):
        
        ''' this method finds the distance between 2 airports(given by code), 
        by invokeong the greateCirlceList above  '''
        
        self.code1 = code1
        self.code2 = code2
        
        self.object1 = self.airport_dict[self.code1] # finding the first airport object stored in the dictonary
        self.lat1 = self.object1.latitude
        self.long1 = self.object1.longitude
        
        self.object2 = self.airport_dict[self.code2] # finding the second airport object stored in the dictonary
        self.lat2 = self.object2.latitude
        self.long2 = self.object2.longitude
        
        self.distance_between = AirportAtlas.greatCircledList(self.lat1, self.long1, self.lat2, self.long2)
        return self.distance_between
    
    
    def getCostOfTrip(self, start, destination, currency_obj, currency_rate_obj):
        
        ''' Given the starting and ending destinations, this method finds the cost of a single trip '''
        
        self.start = start
        self.destination = destination
        self.currency_obj = currency_obj
        self.currency_rate_obj = currency_rate_obj
        
        self.name_country = self.airport_dict[self.start] #getting the names of the start country
        self.name_country = self.name_country.country 

        #find the currency code for the country given the name of the country 
        self.currency_code = self.currency_obj.currency_dict[self.name_country]
        self.currency_rate = float(self.currency_rate_obj.currency_rate_dict[self.currency_code])

        self.distance = self.getDistanceBetweenAirports(self.start, self.destination) #get the distance 
        self.cost = self.distance * self.currency_rate # multiply by currency rate 
        self.cost = int(self.cost) # find the cost 
        
        return self.cost

