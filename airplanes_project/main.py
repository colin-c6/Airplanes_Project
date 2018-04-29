'''
Created on 22 Mar 2018

@author: colin
'''
import sys
from Airport import AirportAtlas
from BestRoute import Itinerary
from Aircrafts import Aircrafts
from Currency import CurrencyRates, Currencys


def main():
    
    ''' Main Function that controls the flow of the program.'''
    
    atlas_obj = AirportAtlas('./data/airport.csv') 
    currency_obj = Currencys('./data/countrycurrency.csv') # initalising the currency and currency rate classes which makes 
    rate_obj = CurrencyRates('./data/currencyrates.csv') # dictonaries for these.
    aircraft_obj = Aircrafts('./data/aircraft.csv')   
    test_itinerary_obj = Itinerary(aircraft_obj,atlas_obj ,currency_obj ,rate_obj)
    
    if len(sys.argv) > 1: #To read a csv inputted from the command line 
        test_itinerary_obj.findBestRoute(sys.argv[1])
    else: #local testRouteData file I have 
        test_itinerary_obj.findBestRoute('./data/testRouteData.csv')

if __name__ == '__main__':
    main()