from __future__ import annotations

from typing import TYPE_CHECKING
from functools import lru_cache

from typing import Optional

from .objproxy import DefaultOSAObjProxy
from .helper_bridging import HelperScript



class Application(DefaultOSAObjProxy):
    def __init__(self, name: Optional[str] = None, helper_script: Optional[HelperScript] = None, obj_id: Optional[int] = None, class_name: Optional[str] = None):
        if all([helper_script, obj_id, class_name]):
            super().__init__(helper_script, obj_id, class_name)
        elif name is not None:
            helper_script = HelperScript.default
            app = helper_script.get_application(name)
            super().__init__(helper_script, app.obj_id, app.class_name)
        else:
            raise ValueError('`name` or `helper_script`, `obj_id`, `class_name` must be provided')
    
    @property
    def id(self) -> str:
        """The unique identifier of the application."""
        return self._call_method('id')

    @property
    def name(self) -> str:
        """The name of the application."""
        return self._call_method('name') # The name is a function so it needs special handling

    @property
    def frontmost(self) -> bool:
        """Whether the application is currently frontmost."""
        return self._call_method('frontmost')

    def activate(self):
        """Activate the application."""
        return self._call_method('activate')

HelperScript.set_default_class_map({
    'application': Application
})