
from ...osascript import OSAScript
from ...helper_bridging import OSAObjProxy, OSAObjArray
from typing import List
from .record import Record
from .smartgroup import SmartGroup

class Database(OSAObjProxy):
    # elements
    @property
    def contents(self) -> OSAObjArray['Record']:
        """The contents of the database."""
        return self._get_property('contents')

    @property
    def parents(self) -> OSAObjArray['Record']:
        """The parents of the database."""
        return self._get_property('parents')

    @property
    def records(self) -> OSAObjArray['Record']:
        """The records contained in the database."""
        return self._get_property('records')

    @property
    def smart_groups(self) -> OSAObjArray['SmartGroup']:
        """The smart groups contained in the database."""
        return self._get_property('smartGroups')

    # TODO: tag_groups
    # @property
    # def tag_groups(self) -> List[TagGroup]:
    #     """The tag groups contained in the database."""
    #     return self.get_property_native('tagGroups')

    # properties
    @property
    def annotations_group(self) -> 'Record':
        """The group for annotations, will be created if necessary."""
        return self._get_property('annotationsGroup')

    @property
    def comment(self) -> str:
        """The comment of the database."""
        return self._call_method('comment')
    
    @comment.setter
    def comment(self, value: str):
        self._set_property('comment', value)

    @property
    def current_group(self) -> 'Record':
        """The (selected) group of the frontmost window. Returns root if no current group exists."""
        return self._get_property('currentGroup')

    @property
    def encrypted(self) -> bool:
        """Specifies if a database is encrypted or not."""
        return self._call_method('encrypted')

    @property
    def id(self) -> int:
        """The scripting identifier of a database."""
        return self._call_method('id')

    @property
    def incoming_group(self) -> 'Record':
        """The default group for new notes. Might be identical to root."""
        return self._get_property('incomingGroup')

    @property
    def name(self) -> str:
        """The name of the database."""
        return self._call_method('name')
    
    @name.setter
    def name(self, value: str):
        self._set_property('name', value)

    @property
    def path(self) -> str:
        """The POSIX path of the database."""
        return self._call_method('path')

    @property
    def read_only(self) -> bool:
        """Specifies if a database is read-only and can't be modified."""
        return self._call_method('readOnly')

    @property
    def root(self) -> 'Record':
        """The top level group of the database."""
        return self._get_property('root')

    @property
    def sync_group(self) -> 'Record':
        """Obsolete group for synchronizing with DEVONthink To Go 1.x."""
        raise NotImplementedError()

    @property
    def tags_group(self) -> 'Record':
        """The group for tags."""
        return self._get_property('tagsGroup')

    @property
    def trash_group(self) -> 'Record':
        """The trash's group."""
        return self._get_property('trashGroup')

    @property
    def uuid(self) -> str:
        """The unique and persistent identifier of a database for external referencing."""
        return self._call_method('uuid')
    
    def __repr__(self):
        return f'<Database {self.name}>'