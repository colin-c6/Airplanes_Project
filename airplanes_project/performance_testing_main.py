'''
Created on 22 Mar 2018

@author: colin
'''
from pathlib import Path
from Airport import AirportAtlas
from exhaustive_algo import Itinerary
from greedy_algo import GreedyItinery
from Aircrafts import Aircrafts
from Currency import CurrencyRates, Currencys
import time
import matplotlib.pyplot as plt





def main():
    
    ''' Main Function that controls the flow of the program.'''
    
    atlas_obj = AirportAtlas('./data/airport.csv') 
    currency_obj = Currencys('./data/countrycurrency.csv') # initalising the currency and currency rate classes which makes 
    rate_obj = CurrencyRates('./data/currencyrates.csv') # dictonaries for these.
    aircraft_obj = Aircrafts('./data/aircraft.csv')   
    test_itinerary_obj_exhaustive = Itinerary(aircraft_obj,atlas_obj ,currency_obj ,rate_obj)
    
     
    linear_time = []
    pathlist = Path('./performance_testing').glob('**/*.csv')
    for file in pathlist:
        start = time.time()
        test_itinerary_obj_exhaustive.findBestRoute(file)
        end = time.time()
        run_time = end - start
        linear_time.append(run_time)
 
    plt.figure(1)
    plt.plot(linear_time)
    plt.xlabel("Size of N (exhaustive)")
    plt.ylabel("Time")
    plt.title("Exhaustive Search Performance")
    plt.savefig('exhaustive_search.png')
 
     
     
    test_itinerary_obj_greedy = GreedyItinery(aircraft_obj,atlas_obj ,currency_obj ,rate_obj)
    linear_time_greedy = []
    pathlist_greedy = Path('./performance_testing').glob('**/*.csv')
    for files in pathlist_greedy:
        start_greedy = time.time()
        test_itinerary_obj_greedy.findBestRoute(files)
        end_greedy = time.time()
        run_time_greedy = end_greedy - start_greedy
        linear_time_greedy.append(run_time_greedy)

        
    plt.figure(2)
    plt.plot(linear_time_greedy)
    plt.xlabel("Size of N (greedy)")
    plt.ylabel("Time")
    plt.title("Greedy Performance")
    plt.savefig('greedy_search.png')

    plt.show()
    
if __name__ == '__main__':
    main()