import unittest
import typing
import logging
from pydt3 import DEVONthink3
from pydt3.apps.devonthink.record import Record
from pydt3.apps.devonthink.text import Text

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class TestRecord(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        dbs = DEVONthink3().databases
        assert len(dbs) > 0, "No databases found"
        print("AAAA")
        print(dbs[0].name)
        self.dbs = dbs
        self.records = [record for db in dbs for record in db.contents]
    
    def test_general(self):
        record: Record
        for record in self.records:
            # record: Record
            self.assertTrue(isinstance(record, Record))
            self.assertTrue(isinstance(record.uuid, str))
            self.assertTrue(isinstance(record.name, str))
            self.assertTrue(isinstance(record.path, str))
            self.assertTrue(isinstance(record.plain_text, str))
            self.assertTrue(isinstance(record.rich_text, (Text, type(None))))
    
    def test_children(self):
        for record in self.records:
            children = record.children
            self.assertTrue(isinstance(children, typing.Sequence))
            self.assertTrue(all(isinstance(child, Record) for child in children))

    def test_incoming_references(self):
        for record in self.records:
            incoming_references = record.incoming_references
            self.assertTrue(isinstance(incoming_references, typing.Sequence))
            self.assertTrue(all(isinstance(incoming_reference, Record) for incoming_reference in incoming_references))

    def test_outgoing_references(self):
        for record in self.records:
            outgoing_references = record.outgoing_references
            self.assertTrue(isinstance(outgoing_references, typing.Sequence))
            self.assertTrue(all(isinstance(outgoing_reference, Record) for outgoing_reference in outgoing_references))

    def test_parents(self):
        for record in self.records:
            parents = record.parents
            self.assertTrue(isinstance(parents, typing.Sequence))
            self.assertTrue(all(isinstance(parent, Record) for parent in parents))

    def test_addition_date(self):
        for record in self.records:
            addition_date = record.addition_date
            self.assertTrue(isinstance(addition_date, str))

    def test_aliases(self):
        for record in self.records:
            aliases = record.aliases
            self.assertTrue(isinstance(aliases, str))

    def test_all_document_dates(self):
        for record in self.records:
            all_document_dates = record.all_document_dates
            if all_document_dates is not None:
                self.assertTrue(isinstance(all_document_dates, typing.Sequence))
                self.assertTrue(all(isinstance(date, str) for date in all_document_dates))
    
