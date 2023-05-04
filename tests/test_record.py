import unittest
import typing
import logging
from pydt3 import DEVONthink3

from . import utils

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class TestRecord(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        dbs = DEVONthink3().databases
        assert len(dbs) > 0, "No databases found"
        self.dbs = dbs
    
    def test_properties(self):
        for db in self.dbs:
            for record in db.contents:
                if record.reference_url != 'x-devonthink-item://884BBB5B-5629-4C5D-825A-C3844F9B8754':
                    continue
                utils._test_obj_properties(record, skips=('data', 'web_archive', 'source', 'paginated_pdf', 'image', 'thumbnail', 'plain_text', 'rich_text'))
            



if __name__ == '__main__':
    unittest.main()