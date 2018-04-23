'''
Created on 22 Mar 2018

@author: colin
'''
from Airport import AirportAtlas
from BestRoute import Itinerary
from Aircrafts import Aircrafts


def main():
    
    ''' Main Function that controls the flow of the program.'''
    
    atlas = AirportAtlas('./data/airport.csv') 
    aircraftPass = Aircrafts('./data/aircraft.csv')   
    test_itinerary = Itinerary(aircraftPass,atlas)
    test_itinerary.findBestRoute('./data/testRouteData.csv')
    #print(atlas.getCostOfTrip('ELU', 'EGR'))
    
if __name__ == '__main__':
    main()