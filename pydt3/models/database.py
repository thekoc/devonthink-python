
from ..osascript import OSAScript, OSAObjProxy
from typing import List
from .record import Record
from .smartgroup import SmartGroup

class Database(OSAObjProxy):
    def __init__(self, script: 'OSAScript', obj_id: int, class_name: str):
        super().__init__(script, obj_id, class_name)
        
    # elements
    @property
    def contents(self) -> List['Record']:
        """The contents of the database."""
        return self.get_property_native('contents')

    @property
    def parents(self) -> List['Record']:
        """The parents of the database."""
        return self.get_property_native('parents')

    @property
    def records(self) -> List['Record']:
        """The records contained in the database."""
        return self.get_property_native('records')

    @property
    def smart_groups(self) -> List['SmartGroup']:
        """The smart groups contained in the database."""
        return self.get_property_native('smartGroups')

    # @property
    # def tag_groups(self) -> List[TagGroup]:
    #     """The tag groups contained in the database."""
    #     return self.get_property_native('tagGroups')

    # properties
    @property
    def annotations_group(self) -> 'Record':
        """The group for annotations, will be created if necessary."""
        return self.get_property_native('annotationsGroup')

    @property
    def comment(self) -> str:
        """The comment of the database."""
        return self.get_property_native('comment')
    
    @comment.setter
    def comment(self, value: str):
        self.set_property('comment', value)

    @property
    def current_group(self) -> 'Record':
        """The (selected) group of the frontmost window. Returns root if no current group exists."""
        return self.get_property_native('currentGroup')

    @property
    def encrypted(self) -> bool:
        """Specifies if a database is encrypted or not."""
        return self.get_property_native('encrypted')

    @property
    def id(self) -> int:
        """The scripting identifier of a database."""
        return self.get_property_native('id')

    @property
    def incoming_group(self) -> 'Record':
        """The default group for new notes. Might be identical to root."""
        return self.get_property_native('incomingGroup')

    @property
    def name(self) -> str:
        """The name of the database."""
        return self.get_property_native('name')
    
    @name.setter
    def name(self, value: str):
        self.set_property('name', value)

    @property
    def path(self) -> str:
        """The POSIX path of the database."""
        return self.get_property_native('path')

    @property
    def read_only(self) -> bool:
        """Specifies if a database is read-only and can't be modified."""
        return self.get_property_native('readOnly')

    @property
    def root(self) -> 'Record':
        """The top level group of the database."""
        return self.get_property_native('root')

    @property
    def sync_group(self) -> 'Record':
        """Obsolete group for synchronizing with DEVONthink To Go 1.x."""
        raise NotImplementedError()

    @property
    def tags_group(self) -> 'Record':
        """The group for tags."""
        return self.get_property_native('tagsGroup')

    @property
    def trash_group(self) -> 'Record':
        """The trash's group."""
        return self.get_property_native('trashGroup')

    @property
    def uuid(self) -> str:
        """The unique and persistent identifier of a database for external referencing."""
        return self.get_property_native('uuid')
    
    def __repr__(self):
        return f'<Database {self.name}>'


OSAObjProxy._NAME_CLASS_MAP['database'] = Database