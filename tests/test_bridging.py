import unittest
import logging

from pydt3 import DEVONthink3
from pydt3.apps.devonthink.database import Database
from pydt3.helper_bridging import OSAObjArray, HelperScript

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

class TestBridging(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.script = HelperScript.default
