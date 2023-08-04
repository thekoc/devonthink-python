import os
from functools import lru_cache

from .osascript import OSAScript, DefaultOSAObjProxy

SCRIPT_PATH = os.path.join(os.path.dirname(__file__), 'jxa_helper.scpt')


class Application(DefaultOSAObjProxy):
    def __init__(self, name) -> None:
        self.script = OSAScript.from_path(SCRIPT_PATH)
        response = self.script.call_json('getApplication', {'name': name})
        super().__init__(self.script, response['objId'], response['className'])
        self._associsated_application = self

    @property
    def id(self) -> str:
        """The unique identifier of the application."""
        return self.get_property_native('id')()
    
    @property
    def name(self) -> str:
        """The name of the application."""
        return self.get_property_native('name')() # The name is a function so it needs special handling

    @property
    def frontmost(self):
        """Whether the application is currently frontmost."""
        return self.get_property_native('frontmost')()

    def activate(self):
        """Activate the application."""
        self.call_method('activate')

    @lru_cache(maxsize=64)
    def parent_of_class(self, name: str):
        """Get the parent of the application of the specified class."""
        return self.call_method('parentOfClass', args=[name])