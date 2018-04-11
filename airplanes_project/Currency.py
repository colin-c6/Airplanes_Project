import os
import csv
from functools import lru_cache

class Currencys():
    
    
    ''' class creates  currency dictonary'''
    
    currency_dict= {} 
    def __init__(self, currencyCountryFile):
        
        ''' initalising method that invokes the method to make the currency dictonary'''

        self.currencyCountryFile = currencyCountryFile
        self.getCountryDict(self.currencyCountryFile)
        
    @lru_cache(maxsize=2)
    def getCountryDict(self, countryFile):
        
        ''' this method accepts the currency file and creates a dictonary'''
        
        self.countryFile = countryFile
        with open(os.path.join(self.countryFile),"rt", encoding="utf8" ) as countryFile: # r is for reading the file
            self.country_csv_reader = csv.reader(countryFile) 
            self.currency_dict = {column[0] : column[14] for column in self.country_csv_reader}
        
        return self.currency_dict


        
class CurrencyRates():
    
    '''class that creates the currency rates dictonary '''
    currencyRate_dict= {}
    
    def __init__(self, currencyRateFile):
        
        ''' initalizing method that accepts the currencyRate file and invokes the method 
        to create the currency rate dictonary'''
        
        self.currencyRateFile = currencyRateFile
        self.getRateDict(self.currencyRateFile)
    
    
        
    @lru_cache(maxsize=2)
    def getRateDict(self, RateFile):
        
        ''' this method creates the currency rate dictonary '''
        
        self.RateFile = RateFile
        with open(os.path.join(self.RateFile),"rt", encoding="utf8" ) as RateFile: # r is for reading the file
            self.rate_csv_reader = csv.reader(RateFile)
            self.currencyRate_dict = {column[1] : column[2] for column in self.rate_csv_reader}
        
        
        return self.currencyRate_dict