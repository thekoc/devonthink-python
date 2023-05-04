import unittest
import typing
import logging
from pydt3 import DEVONthink3

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class TestDatabase(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        dbs = DEVONthink3().databases
        assert len(dbs) > 0, "No databases found"
        self.dbs = dbs
    
    def test_properties(self):
        for db in self.dbs:
            self._test_db(db)
    
    def _test_db(self, db):
        obj = db
        type_ = type(obj)
        for name in dir(type_):
            try:
                if name.startswith('_'):
                    continue
                if isinstance(getattr(type_, name), property):
                    logger.info(f"Testing {obj}.{name}")
                    returned_value = getattr(obj, name)
                    returned_type = typing.get_type_hints(getattr(type_, name).fget)['return']
                    generic_origin = typing.get_origin(returned_type)
                    if generic_origin is not None and generic_origin is list:
                        generic_args = typing.get_args(returned_type)
                        assert len(generic_args) == 1, f"Expected 1 generic argument, got {len(generic_args)}"
                        self.assertTrue(all(isinstance(value, generic_args[0]) for value in returned_value), f"Expected all values of {type_}.{name} to be of type {generic_args[0]}, got {returned_value}")
                    else:
                        self.assertIsInstance(returned_value, returned_type)
            except NotImplementedError:
                continue

            



if __name__ == '__main__':
    unittest.main()