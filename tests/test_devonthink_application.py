import unittest
import logging
import typing

from pydt3 import DEVONthink3
from pydt3.application import Application
from pydt3.apps.devonthink.database import Database
from pydt3.osascript import OSAObjArray

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

class TestDEVONhinkApplication(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.app = DEVONthink3()

    def test_id(self):
        print(self.app.id)
        self.assertTrue(self.app.id == 'com.devon-technologies.think3')
        
    def test_name(self):
        self.assertTrue(self.app.name == 'DEVONthink 3')
    
    def test_databases(self):
        dbs  = self.app.databases
        self.assertTrue(isinstance(dbs, OSAObjArray))
        self.assertTrue(len(dbs) > 0)
        self.assertTrue(all(isinstance(db, Database) for db in dbs))


if __name__ == '__main__':
    unittest.main()