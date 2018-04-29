import unittest
from airplanes_project import Aircrafts


class Test_Aircraft(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.aircraft = Aircrafts.Aircrafts('./airplanes_test_input.csv')
        
    def test_aircraft_dict(self):
        '''This function tests that the aircraft dictionary is being constructor as expected'''
        
        self.assertEqual(self.aircraft.aircraft_dict['737'],21613.4362,"Dictionary not successfully created")
        self.assertEqual(self.aircraft.aircraft_dict['A330'],'13430',"Dictionary not successfully created")
        
    def test_metrics_conversion(self):
            
        ''' This function checks that the metrics conversion is accurate'''

        self.assertEqual(self.aircraft.metricsConversion("imperial",1), 1.60934, "Not sucessfully converted")
        self.assertEqual(self.aircraft.metricsConversion("metric",1),1, "Not sucessfully converted")
        self.assertEqual(self.aircraft.metricsConversion("imperial",20), 32.1868, "Not sucessfully converted")
        self.assertEqual(self.aircraft.metricsConversion("metric",20), 20, "Not sucessfully converted")
        self.assertEqual(self.aircraft.metricsConversion("imperial",-5), -8.0467, "Not sucessfully converted")
        self.assertEqual(self.aircraft.metricsConversion("metric",-5), -5, "Not sucessfully converted")
        
    
    def test_airplane_fuel_check(self):
        
        self.assertTrue(self.aircraft.airplanePassFuel(15000, '737'),"the airplane didnt pass the test")
        self.assertFalse(self.aircraft.airplanePassFuel(25000000000, '737'),"the airplane didnt pass the test")
       
       
if __name__ == '__main__':
    unittest.main()