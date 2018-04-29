import os
import csv
from functools import lru_cache

class Currencys():
    
    ''' class creates  currency dictonary'''
    
    currency_dict= {} 
    
    def __init__(self, currency_country_file):
        
        ''' initalizing method that invokes the method to make the currency dictionary'''

        self.currency_country_file = currency_country_file
        self.getCountryDict(self.currency_country_file)
        
    @lru_cache(maxsize=2)
    def getCountryDict(self, country_file):
        
        ''' this method accepts the currency file and creates a dictonary'''
        
        self.country_file = country_file
        with open(os.path.join(self.country_file),"rt", encoding="utf8" ) as country_file: # r is for reading the file
            self.country_csv_reader = csv.reader(country_file) 
            self.currency_dict = {column[0] : column[14] for column in self.country_csv_reader}
        
        return self.currency_dict


        
class CurrencyRates():
    
    '''class that creates the currency rates dictonary '''
    currency_rate_dict= {}
    
    def __init__(self, currency_rate_file):
        
        ''' initalizing method that accepts the currencyRate file and invokes the method 
        to create the currency rate dictonary'''
        
        self.currency_rate_file = currency_rate_file
        self.getRateDict(self.currency_rate_file)
    
    
        
    @lru_cache(maxsize=2)
    def getRateDict(self, rate_file):
        
        ''' this method creates the currency rate dictonary '''
        
        self.rate_file = rate_file
        with open(os.path.join(self.rate_file),"rt", encoding="utf8" ) as rate_file: # r is for reading the file
            self.rate_csv_reader = csv.reader(rate_file)
            self.currency_rate_dict = {column[1] : column[2] for column in self.rate_csv_reader}
        
        
        return self.currency_rate_dict