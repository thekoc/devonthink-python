import datetime
import unittest
import typing
import logging
from pydt3 import DEVONthink3
from pydt3.apps.devonthink.record import Record
from pydt3.apps.devonthink.reminder import Reminder
from pydt3.apps.devonthink.text import Text

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class TestRecord(unittest.TestCase):
    def setUp(self) -> None:
        self.app = DEVONthink3()
        dbs = self.app.databases
        assert len(dbs) > 0, "No databases found"
        self.dbs = [db for db in dbs if db.name == "test-db"]
        self.records: typing.Sequence[Record] = [record for db in self.dbs for record in db.contents]


    def tearDown(self) -> None:
        pass
    
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
            self.assertTrue(isinstance(record.reminder, (Reminder, type(None))))
            self.assertTrue(isinstance(record.type, str))
            self.assertTrue(isinstance(record.modification_date, datetime.datetime))
            self.assertTrue(isinstance(record.addition_date, datetime.datetime))
            self.assertTrue(isinstance(record.creation_date, datetime.datetime))
    
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
            self.assertTrue(isinstance(addition_date, datetime.datetime))

    def test_aliases(self):
        for record in self.records:
            aliases = record.aliases
            self.assertTrue(isinstance(aliases, str))

    def test_altitude(self):
        for record in self.records:
            altitude = record.altitude
            self.assertTrue(isinstance(altitude, (int, float)))

    def test_tags(self):
        for record in self.records:
            tags = record.tags
            self.assertTrue(isinstance(tags, typing.Sequence))
            self.assertTrue(all(isinstance(tag, str) for tag in tags))
    
    def test_all_document_dates(self):
        for record in self.records:
            # record: Record
            all_document_dates = record.all_document_dates
            if all_document_dates is not None:
                self.assertTrue(isinstance(all_document_dates, typing.Sequence))
                self.assertTrue(all(isinstance(date, datetime.datetime) for date in all_document_dates))
    
    def test_annotation(self):
        for record in self.records:
            annotation = record.annotation
            self.assertTrue(isinstance(annotation, (Record, type(None))))

        # Test setting annotation
        test_record = self.app.create_record_with({
            "name": "unittest_record",
            "type": "text",
        })

        annotation = self.app.create_record_with({
            "name": "unittest_annotation",
            "type": "text",
            'plain text': 'This is a test annotation'
        })

        test_record.annotation = annotation
        self.assertTrue(test_record.annotation.uuid == annotation.uuid)

        self.app.delete(test_record)
        self.app.delete(annotation)
    
    def test_annotation_count(self):
        for record in self.records:
            annotation_count = record.annotation_count
            self.assertTrue(isinstance(annotation_count, int))