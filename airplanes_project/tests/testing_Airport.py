import unittest
from airplanes_project import Airport, Currency



class Test_Aircraft(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        
        ''' Setting up the tests by creating the airport, currency and currency rate objects required'''
        
        self.airport_obj = Airport.AirportAtlas('./airport_test_input.csv')
        self.currency_obj = Currency.Currencys('./currency_test_input.csv')
        self.currency_rate_obj = Currency.CurrencyRates('./currency_rate_test_input.csv')
        
        
    def test_airport_dict(self):
        
        '''This function tests that the airport atlas dictionary is being constructor as expected'''
        
        self.assertIsInstance(self.airport_obj.airport_dict['DUB'], object, "Airport Object not sucessfully placed in diconary")
        self.assertNotIsInstance(self.airport_obj.airport_dict['DUB'], int, "Airport Object not sucessfully placed in diconary")
        self.assertEqual(self.airport_obj.airport_dict['DUB'].country, 'Ireland', "Airport Object contains incorrect values")
        self.assertNotEqual(self.airport_obj.airport_dict['DUB'].country, 'Dublin', "Airport Object contains incorrect values")
        self.assertEqual(self.airport_obj.airport_dict['DUB'].latitude, '53.421333' , "Airport Object contains incorrect values")
        self.assertEqual(self.airport_obj.airport_dict['DUB'].longitude, '-6.270075', "Airport Object contains incorrect values")

    
    def test_airport(self):

        ''' This function tests that the correct airport is returned '''
        
        self.assertIsInstance(self.airport_obj.getAirport('DUB'),object,"Incorrect object returned")
        self.assertNotIsInstance(self.airport_obj.getAirport('DUB'), int,"Incorrect object returned")
    
    
    
    def test_greatCircledList(self):
        
        ''' this test checks that the greatCircledList returns the correct values '''
        
        self.assertEqual(self.airport_obj.greatCircledList('53.421333', '-6.270075' ,'40.639751' , '-73.778925'),5103.02675898737 ,"Distance incorrect")
        self.assertNotEqual(self.airport_obj.greatCircledList('53.421333', '-6.270075' ,'40.639751' , '-73.778925'),'5103.02675898737' ,"Distance incorrect")
        self.assertEqual(self.airport_obj.greatCircledList(53.421333, -6.270075 ,40.639751 , -73.778925),5103.02675898737 ,"Distance incorrect")
        self.assertEqual(self.airport_obj.greatCircledList('53.421333', '-6.270075' ,40.639751 , -73.778925),5103.02675898737 ,"Distance incorrect")
        self.assertNotEqual(self.airport_obj.greatCircledList('53.421333', '-6.270075' ,40.639751 , -73.778925),10 ,"Distance incorrect")
        
        
    
    def test_getDistanceBetweenAirports(self):
        
        ''' This test checks that the distance between two airports is calucalted correctly'''
        
        self.assertEqual(self.airport_obj.getDistanceBetweenAirports('DUB', 'JFK'),5103.02675898737 ,"Distance incorrect")
        self.assertNotEqual(self.airport_obj.getDistanceBetweenAirports('DUB', 'JFK'),55,"Distance incorrect")
        self.assertNotEqual(self.airport_obj.getDistanceBetweenAirports('DUB', 'JFK'),'5103.02675898737',"Distance incorrect")
        
        
    def test_getCostOfTrip(self):
        
        ''' this checks that the correct cost is obtained when two cities and the required currency objects are supplied '''
        
        self.assertEqual(self.airport_obj.getCostOfTrip('DUB', 'JFK', self.currency_obj, self.currency_rate_obj),5103 ,"Distance incorrect")
        self.assertEqual(self.airport_obj.getCostOfTrip('JFK', 'DUB', self.currency_obj, self.currency_rate_obj), 4841 ,"Distance incorrect")
        
        
        
if __name__ == '__main__':
    unittest.main()