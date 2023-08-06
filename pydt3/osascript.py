import json
from logging import getLogger
from typing import Any, Optional, TypeVar, Sequence, Generic, TYPE_CHECKING
from Foundation import NSAppleScript, NSURL, NSAppleEventDescriptor


if TYPE_CHECKING:
    from .application import Application

logger = getLogger(__name__)

class OSAObjProxy:
    _NAME_CLASS_MAP = {}
    _osaobj_rc = {} # {id(script): {obj_id: count}}

    script = None
    obj_id = None
    class_name = None
    
    def __init__(self, script: 'OSAScript', obj_id: int, class_name: str):
        self.script = script
        self.obj_id = obj_id
        self.class_name = class_name
        self._associsated_application = None
        # reference count plus one
        self._osaobj_rc.setdefault(id(script), {}).setdefault(obj_id, 0)
        self._osaobj_rc[id(script)][obj_id] += 1 
    
    @property
    def binded_application(self) -> Optional['Application']:
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
    def pyobj_to_json(cls, obj):
        if isinstance(obj, (int, float, str, bool, type(None))):
            return {
                'type': 'plain',
                'data': obj
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
    
class OSAScript:
    def __init__(self, script: NSAppleScript):
        self.script = script

    @classmethod
    def from_path(cls, path):
        url = NSURL.fileURLWithPath_(path)
        script, error = NSAppleScript.alloc().initWithContentsOfURL_error_(url, None)
        if error:
            raise RuntimeError(error)
        return cls(script)
    
    def call(self, func_name: str, param: str):
        script = self.script
        event = NSAppleEventDescriptor.appleEventWithEventClass_eventID_targetDescriptor_returnID_transactionID_(
            self.fourcharcode(b'ascr'), self.fourcharcode(b'psbr'), NSAppleEventDescriptor.nullDescriptor(), 0, 0)
        descriptor_list = NSAppleEventDescriptor.listDescriptor()
        descriptor_list.insertDescriptor_atIndex_(NSAppleEventDescriptor.descriptorWithString_(param), 0)
        event.setDescriptor_forKeyword_(descriptor_list, self.fourcharcode(b'----'))

        event.setDescriptor_forKeyword_(NSAppleEventDescriptor.descriptorWithString_(func_name), self.fourcharcode(b'snam'))

        result, error = script.executeAppleEvent_error_(event, None)
        if error:
            raise RuntimeError(error)
        else:
            return result.stringValue()
    
    def call_json(self, func_name: str, param: dict):
        param_str = json.dumps(param)
        logger.debug(f'call_json func_name {func_name} param: {param_str}')
        result = self.call(func_name, param_str)
        logger.debug(f'call_json result: {result}')
        return json.loads(result)
    
    def get_properties(self, obj_id: int, names: list):
        params = {'objId': obj_id, 'names': names}
        response = self.call_json('getProperties', params)
        return response
    
    def set_properties_values(self, obj_id: int, properties: dict):
        params = {'objId': obj_id, 'properties': properties}
        self.call_json('setPropertyValues', params)
        logger.debug(f'set_properties_values params: {params}')
    
    def fourcharcode(self, chars: bytes):
        return int.from_bytes(chars, 'big')

if __name__ == '__main__':
    script = OSAScript.from_path('/Users/koc/Developer/devonthink/python-api/pydt3/test.scpt')
    print(script.call('echo', 'hello world'))