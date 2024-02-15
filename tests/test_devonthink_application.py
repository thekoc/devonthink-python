import unittest
import logging
import typing
import pydt3.apps.devonthink as dt3

from pydt3 import DEVONthink3
from pydt3.helper_bridging import OSAObjArray

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

class TestDEVONhinkApplication(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.app = DEVONthink3()
        self.dbs = [self.app.ext.db_by_name('blue-book')]

    def test_id(self):
        print(self.app.id)
        self.assertTrue(self.app.id == 'com.devon-technologies.think3')
        
    def test_name(self):
        self.assertTrue(self.app.name == 'DEVONthink 3')
    
    def test_activate(self):
        self.app.activate()
        self.assertTrue(self.app.frontmost, True)
    
    def test_frontmost(self):
        self.assertTrue(isinstance(self.app.frontmost, bool))
    
    def test_databases(self):
        dbs  = self.app.databases
        self.assertTrue(isinstance(dbs, OSAObjArray))
        self.assertTrue(len(dbs) > 0)
        self.assertTrue(all(isinstance(db, dt3.Database) for db in dbs))

if __name__ == '__main__':
    unittest.main()