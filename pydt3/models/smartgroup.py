from .record import Record
from ..osascript import OSAObjProxy, OSAScript

class SmartGroup(Record):
    def __init__(self, script: 'OSAScript', obj_id: int, class_name: str):
        super().__init__(script, obj_id, class_name)

    # properties
    @property
    def exclude_subgroups(self) -> bool:
        """Exclude subgroups of the search group from searching."""
        return self.get_property_native('excludeSubgroups')

    @exclude_subgroups.setter
    def exclude_subgroups(self, value: bool):
        self.set_property('excludeSubgroups', value)

    @property
    def highlight_occurrences(self) -> bool:
        """Highlight found occurrences in documents."""
        return self.get_property_native('highlightOccurrences')

    @highlight_occurrences.setter
    def highlight_occurrences(self, value: bool):
        self.set_property('highlightOccurrences', value)

    @property
    def search_group(self) -> Record:
        """Group of the smart group to search in."""
        return self.get_property_native('searchGroup')

    @search_group.setter
    def search_group(self, value: Record):
        self.set_property('searchGroup', value)

    @property
    def search_predicates(self) -> str:
        """A string representation of the conditions of the smart group."""
        return self.get_property_native('searchPredicates')

    @search_predicates.setter
    def search_predicates(self, value: str):
        self.set_property('searchPredicates', value)

OSAObjProxy._NAME_CLASS_MAP['smartGroup'] = SmartGroup