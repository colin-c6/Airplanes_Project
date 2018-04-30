
import unittest
from airplanes_project import Airport, Currency, Aircrafts, greedy_algo



class Test_Greedy(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
    
        ''' Setting up the required objects '''
    
        self.atlas_obj = Airport.AirportAtlas('./airport_test_input.csv') 
        self.currency_obj = Currency.Currencys('./currency_test_input.csv') # initalising the currency and currency rate classes which makes 
        self.rate_obj = Currency.CurrencyRates('./currency_rate_test_input.csv') # dictonaries for these.
        self.aircraft_obj = Aircrafts.Aircrafts('./airplanes_test_input.csv')   
        self.test_itinerary_obj = greedy_algo.GreedyItinery(self.aircraft_obj, self.atlas_obj, self.currency_obj, self.rate_obj)
        
    def test_createVertices(self):
        
        ''' this function checks that the airport and cities are abstracted from the input'''
        
        self.assertEqual(self.test_itinerary_obj.createVertices(["DUB","GWY","JFK","NOC","KIR"]),\
                         (None, ["DUB","GWY","JFK","NOC","KIR"]),"Function didnt abstract cities correctly")
        
        self.assertEqual(self.test_itinerary_obj.createVertices(["DUB","GWY","JFK","NOC","KIR","737"]),\
               ('737', ["DUB","GWY","JFK","NOC","KIR"]),"Function didnt abstract cities correctly")
        
        self.assertEqual(self.test_itinerary_obj.createVertices(["DUB","GWY","JFK","NOC","","737"]),\
               (None, None),"Function didnt abstract cities correctly")
        
        self.assertEqual(self.test_itinerary_obj.createVertices(["DUB","GWY","JFK","NOC","KIR","xxx"]),\
               (None,["DUB","GWY","JFK","NOC","KIR"]),"Function didnt abstract cities correctly")
        

    def test_aircraftValid(self):
        
        self.assertTrue(self.test_itinerary_obj.checkAircraftValid("737"),"Aircraft is seen as not valid")
        self.assertFalse(self.test_itinerary_obj.checkAircraftValid("BMW"),"Aircraft is seen as not valid")


        
    def test_citiesValid(self):
        
        self.assertTrue(self.test_itinerary_obj.checkCitiesValid(["DUB","GWY","JFK","NOC","KIR"]),"cities is seen as not valid")
        self.assertFalse(self.test_itinerary_obj.checkCitiesValid(["DUB","GWY","Dundalk","NOC","KIR"]),"cities is seen as valid, which is incorrect")

if __name__ == '__main__':
    unittest.main()



