import json
from logging import getLogger
from typing import Any
import weakref
from Foundation import NSAppleScript, NSURL, NSAppleEventDescriptor
logger = getLogger(__name__)

class _PyObjectSpecifier:
    def __init__(self, script: 'OSAScript', obj_id: int):
        self.script = script
        self.obj_id = obj_id
    
    def __call__(self, args=None, kwargs=None) -> Any:
        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        response  = self.script.call_json('callSelf', {
            'objId': self.obj_id,
            'args': [self.script.pyobj_to_json(arg) for arg in args],
            'kwargs': {k: self.script.pyobj_to_json(v) for k, v in kwargs.items()}
        })

        return self.json_to_pyobj(self.script, response)
    
    @classmethod
    def json_to_pyobj(cls, script: 'OSAScript', response: dict):
        if response['type'] == 'value':
            return response['data']
        elif response['type'] == 'reference':
            obj_id = response['objId']
            return cls(script, obj_id)
        elif response['type'] == 'container':
            data = response['data']
            if isinstance(data, list):
                return [
                    cls.json_to_pyobj(script, i) for i in data
                ]
            elif isinstance(data, dict):
                return {
                    k: cls.json_to_pyobj(script, v) for k, v in data.items()
                }

    def __getattr__(self, name: str):
        pass 
    
    
class OSAObjProxy:
    _NAME_CLASS_MAP = {}
    _cached_proxies = {} # {script: {obj_id: proxy}}
    def __init__(self, script: 'OSAScript', obj_id: int, class_name: str):
        self.script = script
        self.obj_id = obj_id
        self.class_name = class_name

    def get_property_raw(self, name: str):
        response = self.script.get_properties(self.obj_id, [name])[name]
        return response

    def set_property(self, name: str, value):
        self.script.set_properties_values(self.obj_id, {name: value})

    def get_property_native(self, name: str):
        return self.json_to_pyobj(self.script, self.get_property_raw(name))
    
    def run_method(self, name: str, args, kwargs: dict = None):
        if kwargs is None:
            kwargs = {}

        kwargs = {k: self.pyobj_to_json(v) for k, v in kwargs.items()}
        args = [self.pyobj_to_json(arg) for arg in args]

        params = {'objId': self.obj_id, 'name': name, 'args': args, 'kwargs': kwargs}
        logger.debug(f'run_method params: {params}')
        response = self.script.call_json('runMethod', params)

        logger.debug(f'run_method response: {response}')

        return self.json_to_pyobj(self.script, response)

    @classmethod
    def json_to_pyobj(cls, script: 'OSAScript', response: dict):
        if response['type'] == 'value':
            return response['data']
        elif response['type'] == 'reference':
            class_name = response['className']
            obj_id = response['objId']
            # Cache the proxy object to avoid creating multiple proxies for the same object
            cached_proxy_ref = cls._cached_proxies.get(id(script), {}).get(obj_id, None)
            if cached_proxy_ref is None:
                reference_cls = cls._NAME_CLASS_MAP.get(class_name, DefaultOSAObjProxy)
                cached_proxy = reference_cls(script, obj_id, class_name)
                cls._cached_proxies.setdefault(id(script), {})[obj_id] = weakref.ref(cached_proxy)
            else:
                cached_proxy = cached_proxy_ref()
            return cached_proxy
        elif response['type'] == 'container':
            data = response['data']
            if isinstance(data, list):
                return [
                    cls.json_to_pyobj(script, i) for i in data
                ]
            elif isinstance(data, dict):
                return {
                    k: cls.json_to_pyobj(script, v) for k, v in data.items()
                }
    
    @classmethod
    def pyobj_to_json(cls, obj):
        if isinstance(obj, (int, float, str, bool, type(None))):
            return {
                'type': 'value',
                'data': obj
            }
        elif isinstance(obj, (list, tuple)):
            return {
                'type': 'container',
                'data': [cls.pyobj_to_json(i) for i in obj]
            }
        elif isinstance(obj, dict):
            return {
                'type': 'container',
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
        logger.debug(f'Releasing object: {self.obj_id} {self.class_name} {self} {id(self)}')
        self.script.call_json('releaseObject', {'objId': self.obj_id})


class DefaultOSAObjProxy(OSAObjProxy):
    def __init__(self, script: 'OSAScript', obj_id: int, class_name: str):
        super().__init__(script, obj_id, class_name)
    
    def __getattr__(self, name):
        return self.get_property_native(name)

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