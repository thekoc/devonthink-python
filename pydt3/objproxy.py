from __future__ import annotations

import logging

from typing import Any, Optional, TypeVar, Sequence, TYPE_CHECKING


if TYPE_CHECKING:
    from .helper_bridging import HelperScript

logger = logging.getLogger(__name__)

class OSAObjProxy:
    def __init__(self, helper_script: Optional[HelperScript] = None, obj_id: Optional[int] = None, class_name: Optional[str] = None):
        self._helper_script: Optional[HelperScript] = helper_script
        self.obj_id: Optional[int] = obj_id
        self.class_name: Optional[str] = class_name
        # reference count plus one
        if self.obj_id is not None:
            self._increase_reference_count()

    def _increase_reference_count(self):
        obj_id = self.obj_id
        if self.obj_id is None:
            raise ValueError('obj_id is None')
        self._helper_script._osaobj_rc.setdefault(obj_id, 0)
        self._helper_script._osaobj_rc[obj_id] += 1
    
    def _decrease_reference_count(self):
        obj_id = self.obj_id
        if self.obj_id is None:
            raise ValueError('obj_id is None')
        self._helper_script._osaobj_rc.setdefault(obj_id, 0)
        self._helper_script._osaobj_rc[obj_id] -= 1
        logger.debug(f'decrease reference count for {obj_id}, current count: {self._helper_script._osaobj_rc[obj_id]}')
        if self._helper_script._osaobj_rc[obj_id] <= 0:
            self._helper_script.release_object_with_id(obj_id)
    
    def bind(self, script: HelperScript, obj_id: int, class_name: str):
        if self.obj_id is not None:
            self._decrease_reference_count()
        self._helper_script = script
        self.obj_id = obj_id
        self.class_name = class_name
        # reference count plus one
        self._increase_reference_count()

    @classmethod
    def from_proxy(cls, proxy: OSAObjProxy):
        return cls(proxy._helper_script, proxy.obj_id, proxy.class_name)

    def _set_property(self, name: str, value):
        return self._helper_script.set_properties(self, {name: value})

    def _get_property(self, name: str):
        return self._helper_script.get_property(self, name)
    
    def _call_method(self, name: str, args = None, kwargs: dict = None):
        return self._helper_script.call_method(self, name, args, kwargs)

    def __del__(self):
        if self.obj_id is not None:
            self._decrease_reference_count()

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self._helper_script.call_self(self, args, kwargs)


T = TypeVar('T')
class OSAObjArray(OSAObjProxy, Sequence[T]):
    """The proxy of the array container in JXA of type `T`
    """

    def whose(self, filter) -> 'OSAObjArray[T]':
        return self._call_method('whose', [filter])
    
    def __len__(self) -> int:
        return self._get_property('length')

    def __getitem__(self, index: int) -> T:
        return self._call_method('at', args=[index])

    def __iter__(self):
        for i in range(len(self)):
            yield self[i]

class DefaultOSAObjProxy(OSAObjProxy):
    def __getitem__(self, key: str):
        return self._get_property(key)
    
    def __setitem__(self, key: str, value):
        return self._set_property(key, value)
    
    def __getattr__(self, name: str):
        return self._get_property(name)
