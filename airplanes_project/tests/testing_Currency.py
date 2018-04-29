import unittest
from airplanes_project import Currency


class Test_Aircraft(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        
        ''' Setting up the tests by creating the airport, currency and currency rate objects required'''
        
        self.currency_obj = Currency.Currencys('./currency_test_input.csv')
        self.currency_rate_obj = Currency.CurrencyRates('./currency_rate_test_input.csv')
        
        
    def test_getCountryDict(self):
        
        '''This function tests that the Currency dictionary is being constructor as expected'''
        
        self.assertEqual(self.currency_obj.currency_dict['Ireland'], 'EUR',"Dictionary not successfully created")
        self.assertNotEqual(self.currency_obj.currency_dict['Ireland'], 'GBP',"Dictionary not successfully created")
        
    
    
    def test_getRateDict(self):
        
        '''This function tests that the Currency Rate dictionary is being constructor as expected'''
        
        self.assertEqual(self.currency_rate_obj.currency_rate_dict['GBP'], '1.4029',"Dictionary not successfully created")
        self.assertNotEqual(self.currency_rate_obj.currency_rate_dict['GBP'], 1.4029,"Dictionary not successfully created")
        self.assertEqual(self.currency_rate_obj.currency_rate_dict['EUR'], '1',"Dictionary not successfully created")

        
if __name__ == '__main__':
    unittest.main()   