import unittest
import logging

from pydt3.application import Application
from pydt3.apps.devonthink.database import Database
from pydt3.helper_bridging import OSAObjArray, HelperScript

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

class TestBridging(unittest.TestCase):
    def setUp(self) -> None:
        self.app = Application('Finder')

    def test_default_osa_obj_proxy(self):
        self.assertEqual(self.app.name, 'Finder')
    
    def test_osa_obj_array(self):
        items = self.app.items
        self.assertTrue(isinstance(items, OSAObjArray))
        for item in items:
            print(item.name)