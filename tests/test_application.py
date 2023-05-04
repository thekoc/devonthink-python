import unittest
import logging
from typing import get_type_hints, get_origin, get_args

from pydt3 import DEVONthink3

logging.basicConfig(level=logging.DEBUG)

class TestApplication(unittest.TestCase):
    def test_creation(self):
        app = DEVONthink3()
        self.assertIsNotNone(app)
        print(app.current_workspace)
        # Test fallback properties
        self.assertTrue(app.includeStandardAdditions)

    def test_properties(self):
        app = DEVONthink3()
        for name in dir(DEVONthink3):
            try:
                if name.startswith('_'):
                    continue
                if isinstance(getattr(DEVONthink3, name), property):
                    returned_value = getattr(app, name)
                    returned_type = get_type_hints(getattr(DEVONthink3, name).fget)['return']
                    generic_origin = get_origin(returned_type)
                    if generic_origin is not None and generic_origin is list:
                        generic_args = get_args(returned_type)
                        assert len(generic_args) == 1, f"Expected 1 generic argument, got {len(generic_args)}"
                        self.assertTrue(all(isinstance(value, generic_args[0]) for value in returned_value), f"Expected all values of DEVONthink3.{name} to be of type {generic_args[0]}, got {returned_value}")
                    else:
                        self.assertIsInstance(returned_value, returned_type)
            except NotImplementedError:
                continue

            

if __name__ == '__main__':
    unittest.main()