import unittest
import os
from db import timesheet
import app

class TestStringMethods(unittest.TestCase):
    
    def setUp(self):
        pass

    def dbTests(self, _ship, _board):
        f =os.remove("unit_test.db")
        testdb = timesheet("unit_test.db")
        csv_data = open("../time-report-42.csv",'rb').read().decode(encoding='utf-8').split('\r\n')
        try:
            app.add_csv_to_database(csv_data)
            
            report = testdb.get_timesheet_report()
            
        except Exception as e:
            self.assertIsNotNone(e) #if we're here we failed

if __name__ == '__main__':
    unittest.main()