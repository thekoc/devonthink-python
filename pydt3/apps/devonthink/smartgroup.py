from .record import Record
from ...osascript import  OSAScript

class SmartGroup(Record):
    # properties
    @property
    def exclude_subgroups(self) -> bool:
        """Exclude subgroups of the search group from searching."""
        return self._call_method('excludeSubgroups')

    @exclude_subgroups.setter
    def exclude_subgroups(self, value: bool):
        self._set_property('excludeSubgroups', value)

    @property
    def highlight_occurrences(self) -> bool:
        """Highlight found occurrences in documents."""
        return self._call_method('highlightOccurrences')

    @highlight_occurrences.setter
    def highlight_occurrences(self, value: bool):
        self._set_property('highlightOccurrences', value)

    @property
    def search_group(self) -> Record:
        """Group of the smart group to search in."""
        return self._get_property('searchGroup')

    @search_group.setter
    def search_group(self, value: Record):
        self._set_property('searchGroup', value)

    @property
    def search_predicates(self) -> str:
        """A string representation of the conditions of the smart group."""
        return self._call_method('searchPredicates')

    @search_predicates.setter
    def search_predicates(self, value: str):
        self._set_property('searchPredicates', value)
