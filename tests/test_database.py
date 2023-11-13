import unittest
import typing
import logging
import re
from pydt3 import DEVONthink3
from pydt3.osascript import OSAScript
from pydt3.helper_bridging import OSAObjProxy, DefaultOSAObjProxy
from pydt3.apps.devonthink.record import Record
from pydt3.apps.devonthink.smartgroup import SmartGroup

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class TestDatabase(unittest.TestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        dbs = DEVONthink3().databases
        assert len(dbs) > 0, "No databases found"
        self.dbs = list(dbs)
    
    def test_contents(self):
        for db in self.dbs:
            contents = db.contents
            self.assertTrue(isinstance(contents, typing.Sequence))
            self.assertTrue(all(isinstance(record, Record) for record in contents))
    
    def test_parents(self):
        for db in self.dbs:
            parents = db.parents
            self.assertTrue(isinstance(parents, typing.Sequence))
            self.assertTrue(all(isinstance(record, Record) for record in parents))

    def test_records(self):
        for db in self.dbs:
            records = db.records
            self.assertTrue(isinstance(records, typing.Sequence))
            self.assertTrue(all(isinstance(record, Record) for record in records))

    def test_smart_groups(self):
        for db in self.dbs:
            smart_groups = db.smart_groups
            self.assertTrue(isinstance(smart_groups, typing.Sequence))
            self.assertTrue(all(isinstance(smart_group, SmartGroup) for smart_group in smart_groups))

    def test_annotations_group(self):
        for db in self.dbs:
            annotations_group = db.annotations_group
            self.assertTrue(isinstance(annotations_group, Record))

    def test_comment(self):
        for db in self.dbs:
            comment = db.comment
            self.assertTrue(isinstance(comment, str))
            # Test the setter method
            old_comment = comment
            db.comment = "test"
            self.assertEqual(db.comment, "test")
            # Revert the change
            db.comment = old_comment

    def test_current_group(self):
        for db in self.dbs:
            current_group = db.current_group
            self.assertTrue(isinstance(current_group, Record))
    def test_encrypted(self):
        for db in self.dbs:
            encrypted = db.encrypted
            self.assertTrue(isinstance(encrypted, bool))

    def test_id(self):
        for db in self.dbs:
            id = db.id
            self.assertTrue(isinstance(id, int))

    def test_incoming_group(self):
        for db in self.dbs:
            incoming_group = db.incoming_group
            self.assertTrue(isinstance(incoming_group, Record))

    def test_name(self):
        for db in self.dbs:
            name = db.name
            self.assertTrue(isinstance(name, str))
            # Test the setter method
            old_name = name
            db.name = "test"
            self.assertEqual(db.name, "test")
            # Revert the change
            db.name = old_name

    def test_path(self):
        for db in self.dbs:
            path = db.path
            self.assertTrue(isinstance(path, str))
            self.assertTrue(re.match(r'^/.*\.dtBase2$', path))

    def test_read_only(self):
        for db in self.dbs:
            read_only = db.read_only
            self.assertTrue(isinstance(read_only, bool))

    def test_root(self):
        for db in self.dbs:
            root = db.root
            self.assertTrue(isinstance(root, Record))

    def test_tags_group(self):
        for db in self.dbs:
            tags_group = db.tags_group
            self.assertTrue(isinstance(tags_group, Record))

    def test_trash_group(self):
        for db in self.dbs:
            trash_group = db.trash_group
            self.assertTrue(isinstance(trash_group, Record))

    def test_uuid(self):
        for db in self.dbs:
            uuid = db.uuid
            self.assertTrue(isinstance(uuid, str), f"{db.name} has uuid {type(uuid)}")

if __name__ == '__main__':
    unittest.main()