from __future__ import annotations

import datetime

from typing import Any, Optional, TypeVar, Sequence, TYPE_CHECKING
from Foundation import NSAppleScript
from .osascript import OSAScript



if TYPE_CHECKING:
    from .application import Application

class OSAObjProxy:
    _NAME_CLASS_MAP = {}
    _osaobj_rc = {} # {id(script): {obj_id: count}}

    script = None
    obj_id = None
    class_name = None
    
    def __init__(self, script: OSAScript, obj_id: int, class_name: str):
        self.script = script
        self.obj_id = obj_id
        self.class_name = class_name
        self._associsated_application = None
        # reference count plus one
        self._osaobj_rc.setdefault(id(script), {}).setdefault(obj_id, 0)
        self._osaobj_rc[id(script)][obj_id] += 1 
    
    @property
    def binded_application(self) -> Optional[Application]:
        return self._associsated_application

    def get_property_raw(self, name: str):
        response = self.script.get_properties(self.obj_id, [name])[name]
        return response

    def set_property(self, name: str, value):
        self.script.set_properties_values(self.obj_id, {name: value})

    def get_property_native(self, name: str):
        pyobj = self.json_to_pyobj(self.script, self.get_property_raw(name), self.binded_application)
        return pyobj
    
    def call_method(self, name: str, args = None, kwargs: dict = None):
        if kwargs is not None:
            kwargs = {k: self.pyobj_to_json(v) for k, v in kwargs.items()}
        else:
            kwargs = {}
        if args is not None:
            args = [self.pyobj_to_json(arg) for arg in args]
        else:
            args = []

        params = {'objId': self.obj_id, 'name': name, 'args': args, 'kwargs': kwargs}
        response = self.script.call_json('callMethod', params)
        pyobj = self.json_to_pyobj(self.script, response, self.binded_application)
        if isinstance(pyobj, OSAObjProxy):
            pyobj._associsated_application = self.binded_application
        return pyobj

    @classmethod
    def json_to_pyobj(cls, script: 'OSAScript', response: dict, associated_application: Optional['Application'] = None):
        if response['type'] == 'plain':
            return response.get('data')
        elif response['type'] == 'date':
            data = response.get('data')
            return datetime.datetime.fromtimestamp(data)
        elif response['type'] == 'reference':
            class_name = response.get('className', None)
            obj_id = response['objId']
            if class_name is not None and class_name.startswith('array::'):
                reference_cls = OSAObjArray
            elif class_name is not None:
                current_class_name = class_name
                reference_cls = None
                while current_class_name is not None:
                    reference_cls = cls._NAME_CLASS_MAP.get(current_class_name)
                    if reference_cls is not None:
                        break
                    if associated_application is not None:
                        current_class_name = associated_application.parent_of_class(current_class_name)
                    else:
                        break

            if reference_cls is None:
                reference_cls = DefaultOSAObjProxy
            
            proxy = reference_cls(script, obj_id, class_name)

            if associated_application is not None and isinstance(proxy, OSAObjProxy):
                proxy._associsated_application = associated_application
            
            assert isinstance(proxy, OSAObjProxy)
            return proxy
        elif response['type'] == 'array':
            data = response['data']
            assert isinstance(data, list)
            return [
                cls.json_to_pyobj(script, i, associated_application) for i in data
            ]
        elif response['type'] == 'dict':
            data = response['data']
            assert isinstance(data, dict)
            return {
                k: cls.json_to_pyobj(script, v, associated_application) for k, v in data.items()
            }
    
    @classmethod
    def pyobj_to_json(cls, obj) -> dict:
        if isinstance(obj, (int, float, str, bool, type(None))):
            return {
                'type': 'plain',
                'data': obj
            }
        elif isinstance(obj, datetime.datetime):
            return {
                'type': 'date',
                'data': obj.timestamp()
            }
        elif isinstance(obj, (list, tuple)):
            return {
                'type': 'array',
                'data': [cls.pyobj_to_json(i) for i in obj]
            }
        elif isinstance(obj, dict):
            return {
                'type': 'dict',
                'data': {k: cls.pyobj_to_json(v) for k, v in obj.items()}
            }
        elif isinstance(obj, OSAObjProxy):
            return {
                'type': 'reference',
                'objId': obj.obj_id
            }
        else:
            raise TypeError(f'Unsupported type: {type(obj)}')
    
    def __del__(self):
        self._osaobj_rc[id(self.script)][self.obj_id] -= 1
        if self._osaobj_rc[id(self.script)][self.obj_id] <= 0:
            self.script.call_json('releaseObject', {'objId': self.obj_id})

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.call_method(name=None, args=args, kwargs=kwargs)

    def as_class(self, cls: 'OSAObjProxy'):
        return cls(self.script, self.obj_id, self.class_name)


T = TypeVar('T')
class OSAObjArray(Sequence[T], OSAObjProxy):
    """The proxy of the array container in JXA of type `T`
    """
    def __init__(self, script: 'OSAScript', obj_id: int, class_name: str):
        super().__init__(script, obj_id, class_name)
        self._cached_array = None

    def whose(self, **kwargs) -> 'OSAObjArray[T]':
        raise NotImplementedError()
    
    def __len__(self) -> int:
        return self.get_property_native('length')

    def __getitem__(self, index: int) -> T:
        return self.call_method('at', args=[index])

    def __iter__(self):
        return iter(self())

class DefaultOSAObjProxy(OSAObjProxy):
    def __init__(self, script: 'OSAScript', obj_id: int, class_name: str):
        super().__init__(script, obj_id, class_name)
    
    def __getattr__(self, name):
        return self.get_property_native(name)

    def __setattr__(self, name, value):
        try:
            super().__setattr__(name, value)
        except AttributeError:
            self.set_property(name, value)
    



class HelperScript(OSAScript):
    _NAME_CLASS_MAP = {}

    def __init__(self, script: NSAppleScript):
        super().__init__(script)

    @classmethod
    def json_to_pyobj(cls, script: 'OSAScript', response: dict, associated_application: Optional['Application'] = None):
        if response['type'] == 'plain':
            return response.get('data')
        elif response['type'] == 'date':
            data = response.get('data')
            return datetime.datetime.fromtimestamp(data)
        elif response['type'] == 'reference':
            class_name = response.get('className', None)
            obj_id = response['objId']
            if class_name is not None and class_name.startswith('array::'):
                reference_cls = OSAObjArray
            elif class_name is not None:
                current_class_name = class_name
                reference_cls = None
                while current_class_name is not None:
                    reference_cls = cls._NAME_CLASS_MAP.get(current_class_name)
                    if reference_cls is not None:
                        break
                    if associated_application is not None:
                        current_class_name = associated_application.parent_of_class(current_class_name)
                    else:
                        break

            if reference_cls is None:
                reference_cls = DefaultOSAObjProxy
            
            proxy = reference_cls(script, obj_id, class_name)

            if associated_application is not None and isinstance(proxy, OSAObjProxy):
                proxy._associsated_application = associated_application
            
            assert isinstance(proxy, OSAObjProxy)
            return proxy
        elif response['type'] == 'array':
            data = response['data']
            assert isinstance(data, list)
            return [
                cls.json_to_pyobj(script, i, associated_application) for i in data
            ]
        elif response['type'] == 'dict':
            data = response['data']
            assert isinstance(data, dict)
            return {
                k: cls.json_to_pyobj(script, v, associated_application) for k, v in data.items()
            }
    
    @classmethod
    def wrap_to_json(cls, obj) -> dict:
        if isinstance(obj, (int, float, str, bool, type(None))):
            return {
                'type': 'plain',
                'data': obj
            }
        elif isinstance(obj, datetime.datetime):
            return {
                'type': 'date',
                'data': obj.timestamp()
            }
        elif isinstance(obj, (list, tuple)):
            return {
                'type': 'array',
                'data': [cls.pyobj_to_json(i) for i in obj]
            }
        elif isinstance(obj, dict):
            return {
                'type': 'dict',
                'data': {k: cls.pyobj_to_json(v) for k, v in obj.items()}
            }
        elif isinstance(obj, OSAObjProxy):
            return {
                'type': 'reference',
                'objId': obj.obj_id
            }
        else:
            raise TypeError(f'Unsupported type: {type(obj)}')
    
    def call_pyobj_io(self, func_name: str, params: dict):
        params = self.pyobj_to_json(params)

        result = self.call_json_io(func_name, params)

        return self.json_to_pyobj(result)
    
    def release_object_with_id(self, id_: int):
        self.call_pyobj_io(
            'externalCall', {
                
            }
        )