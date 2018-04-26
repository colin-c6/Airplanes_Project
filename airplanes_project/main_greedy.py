from Airport import AirportAtlas
from Aircrafts import Aircrafts
from greedy import GreedyItinery

def main():
    
        
    ''' Main Function that controls the flow of the program.'''
    
    atlas = AirportAtlas('./data/airport.csv') 
    aircraftPass = Aircrafts('./data/aircraft.csv') 
    test_itinerary = GreedyItinery(aircraftPass,atlas)
    test_itinerary.findBestRoute('./data/testRouteData.csv')
    
    
    
if __name__ == "__main__":
    main()