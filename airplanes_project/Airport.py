'''
Created on 22 Mar 2018

@author: colin
'''
import os
import csv
from math import pi, sin, cos, acos , ceil
from functools import lru_cache
from Currency import Currencys, CurrencyRates


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
    
    airport_dict = {}
    def __init__(self,csvFile):
        
        ''' Initsalizing method reads in the airports csv file, and creates the airport, 
        currency and curreny rate dictonaries '''
                
        self.csvAirportFile = csvFile
        self.createAirportDict(self.csvAirportFile)
        
        #Create the currency and currency rate dictonaries
        self.get_currency = Currencys('./data/countrycurrency.csv')
        self.get_rates = CurrencyRates('./data/currencyrates.csv')
    
    
    @lru_cache(maxsize=2)
    def createAirportDict(self, csvFile):
        
        ''' Method to create the Airport Dictonary. uses the 3 letter airport code and
        creates airport objects '''
        
        self.csvFile = csvFile
        with open(os.path.join(self.csvFile),"rt", encoding="utf8" ) as csv_file: # r is for reading the file
            self.csv_reader = csv.reader(csv_file) # reader expects values to be seperated by a commma.
                                        # need to iterate over csv_reader at present its just an object in memory
            self.airport_dict = {column[4] : Airport(column[3],column[4],column[6],column[7]) for column in self.csv_reader}
        
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
        distance = int(distance)
        return distance
    
    
    def getDistanceBetweenAirports(self, code1, code2):
        
        ''' this method finds the distance between 2 airports(given by code), 
        by invokeong the greateCirlceList above  '''
        
        self.code1 = code1
        self.code2 = code2
        
        self.object1 = self.airport_dict[self.code1]
        self.lat1 = self.object1.latitude
        self.long1 = self.object1.longitude
        
        self.object2 = self.airport_dict[self.code2]
        self.lat2 = self.object2.latitude
        self.long2 = self.object2.longitude
        self.distance_between = AirportAtlas.greatCircledList(self.lat1, self.long1, self.lat2, self.long2)
        return self.distance_between
    
    
    def getCostOfTrip(self, start, destination):
        
        ''' Given the starting and ending destinations, this method finds the cost of a single trip '''
        
        self.start = start
        self.destination = destination
        
        self.name_country = self.airport_dict[self.start]
        self.name_country = self.name_country.country 
        #find the currency code for the country given the name of the country 
        self.currency_code = self.get_currency.currency_dict[self.name_country]
        self.currency_rate = float(self.get_rates.currencyRate_dict[self.currency_code])

        self.dist = self.getDistanceBetweenAirports(self.start, self.destination)
        self.cost = self.dist * self.currency_rate
        self.cost = int(ceil(self.cost))
        return self.cost

