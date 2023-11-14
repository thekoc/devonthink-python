from __future__ import annotations

import datetime
import json
import os
import logging

from typing import Any, Optional, TypeVar, Sequence, TYPE_CHECKING
from Foundation import NSAppleScript
from .osascript import OSAScript



if TYPE_CHECKING:
    from .application import Application

logger = logging.getLogger(__name__)

DEFAULT_SCRIPT_PATH = os.path.join(os.path.dirname(__file__), 'jxa_helper.scpt')

class OSAObjProxy:
    def __init__(self, script: HelperScript, obj_id: int, class_name: str):
        self._helper_script = script
        self.obj_id = obj_id
        self.class_name = class_name
        self._associated_application = None
        # reference count plus one
        self._helper_script._osaobj_rc.setdefault(obj_id, 0)
        self._helper_script._osaobj_rc[obj_id] += 1 
    
    @property
    def associated_application(self) -> Optional[Application]:
        return self._associated_application

    def _set_property(self, name: str, value):
        return self._helper_script.set_properties(self, {name: value})

    def _get_property(self, name: str):
        return self._helper_script.get_properties(self, [name])[name]
    
    def _call_method(self, name: str, args = None, kwargs: dict = None):
        return self._helper_script.call_method(self, name, args, kwargs)

    def __del__(self):
        if self._helper_script._osaobj_rc.get(self.obj_id) is None:
            return
        self._helper_script._osaobj_rc[self.obj_id] -= 1
        if self._helper_script._osaobj_rc[self.obj_id] <= 0:
            self._helper_script.release_object_with_id(self.obj_id)

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self._helper_script.call_self(self, args, kwargs)


T = TypeVar('T')
class OSAObjArray(Sequence[T], OSAObjProxy):
    """The proxy of the array container in JXA of type `T`
    """
    def __init__(self, script: HelperScript, obj_id: int, class_name: str):
        super().__init__(script, obj_id, class_name)
        self._cached_array = None

    def whose(self, filter) -> 'OSAObjArray[T]':
        return self._call_method('whose', [filter])
    
    def __len__(self) -> int:
        return self._get_property('length')

    def __getitem__(self, index: int) -> T:
        return self._call_method('at', args=[index])

    def __iter__(self):
        return iter(self())

class DefaultOSAObjProxy(OSAObjProxy):
    def __init__(self, script: HelperScript, obj_id: int, class_name: str):
        super().__init__(script, obj_id, class_name)

    def __getitem__(self, key: str):
        return self._get_property(key)
    
    def __setitem__(self, key: str, value):
        return self._set_property(key, value)



class HelperScript(OSAScript):
    _NAME_CLASS_MAP = {}

    default: HelperScript

    def __init__(self, script: NSAppleScript, application: Optional[Application] = None, osaobj_rc: Optional[dict] = None):
        super().__init__(script)
        self._osaobj_rc = {} if osaobj_rc is None else osaobj_rc
        self._within_application = application
    
    def within_application(self, app: Application):
        return HelperScript(self.script, app, self._osaobj_rc)

    def _unwrap_from_json(self, response: dict, associated_application: Optional['Application'] = None):
        if associated_application is None:
            associated_application = self._within_application
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
                    reference_cls = self._NAME_CLASS_MAP.get(current_class_name)
                    if reference_cls is not None:
                        break
                    if associated_application is not None:
                        current_class_name = associated_application.parent_of_class(current_class_name)
                    else:
                        break

            if reference_cls is None:
                reference_cls = DefaultOSAObjProxy
            
            proxy = reference_cls(self.within_application(associated_application), obj_id, class_name)

            if associated_application is not None and isinstance(proxy, OSAObjProxy):
                proxy._associated_application = associated_application
            
            assert isinstance(proxy, OSAObjProxy)
            return proxy

        elif response['type'] == 'array':
            data = response['data']
            assert isinstance(data, list)
            return [
                self._unwrap_from_json(i, associated_application) for i in data
            ]
        elif response['type'] == 'dict':
            data = response['data']
            assert isinstance(data, dict)
            return {
                k: self._unwrap_from_json(v, associated_application) for k, v in data.items()
            }

    def _wrap_to_json(self: HelperScript, obj) -> dict:
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
                'data': [self._wrap_to_json(i) for i in obj]
            }
        elif isinstance(obj, dict):
            return {
                'type': 'dict',
                'data': {k: self._wrap_to_json(v) for k, v in obj.items()}
            }
        elif isinstance(obj, OSAObjProxy):
            return {
                'type': 'reference',
                'objId': obj.obj_id
            }
        else:
            raise TypeError(f'Unsupported type: {type(obj)}')
    
    def _call_func_pyobj_inout(self, func_name: str, params):

        params = self._wrap_to_json(params)
        logger.debug(f'func_name: {func_name}')
        logger.debug(f'params: {params}')

        params = json.dumps(params)
        result = self._call_str(func_name, params)
        logger.debug(f'result: {result}')

        result = json.loads(result)
        return self._unwrap_from_json(result)

    def echo(self, params):
        return self._call_func_pyobj_inout('echo', params)
    
    def release_object_with_id(self, id: int):
        return self._call_func_pyobj_inout('releaseObjectWithId', {'id': id})
    
    def get_application(self, name: str) -> OSAObjProxy:
        return self._call_func_pyobj_inout('getApplication', {'name': name})
    
    def eval_jxa_code_snippet(self, source: str, locals: Optional[dict] = None):
        return self._call_func_pyobj_inout('evalJXACodeSnippet', {'source': source, 'locals': locals})
    
    def eval_applescript_code_snippet(self, source: str, locals: Optional[dict] = None):
        return self._call_func_pyobj_inout('evalAppleScriptCodeSnippet', {'source': source, 'locals': locals})

    def get_properties(self, obj: OSAObjProxy, properties: list):
        return self._call_func_pyobj_inout('getProperties', {'obj': obj, 'properties': properties})

    def set_properties(self, obj: OSAObjProxy, key_values: dict):
        return self._call_func_pyobj_inout('setProperties', {'obj': obj, 'keyValues': key_values})
    
    def call_method(self, obj: OSAObjProxy, name: str, args = None, kwargs: dict = None):
        return self._call_func_pyobj_inout('callMethod', {'obj': obj, 'name': name, 'args': args, 'kwargs': kwargs})

    def call_self(self, obj: OSAObjProxy, args = None, kwargs: dict = None):
        return self._call_func_pyobj_inout('callSelf', {'obj': obj, 'args': args, 'kwargs': kwargs})

HelperScript.default = HelperScript.from_path(DEFAULT_SCRIPT_PATH)

if __name__ == '__main__':
    script = HelperScript.from_path('/Users/koc/Developer/devonthink/python-api/pydt3/jxa_helper.scpt')
    # print(script.call_func_pyobj_inout('echo', 'hello world'))
    print(script._call_func_pyobj_inout('echo', {'a': 1, 'b': 2}))
    print(script._call_func_pyobj_inout('echo', [1, 2, 3]))
    print(script._call_func_pyobj_inout('echo', datetime.datetime.now()))
    print(script._call_func_pyobj_inout('echo', {'a': 1, 'b': 2, 'c': datetime.datetime.now()}))
    print(script._call_func_pyobj_inout('echo', {'a': 1, 'b': 2, 'c': [1, 2, 3]}))
    print(script._call_func_pyobj_inout('echo', {'a': 1, 'b': 2, 'c': {'d': 1, 'e': 2}}))
    print(script._call_func_pyobj_inout('echo', {'a': 1, 'b': 2, 'c': {'d': 1, 'e': 2, 'f': [1, 2, 3]}}))
    print(script._call_func_pyobj_inout('echo', {'a': 1, 'b': 2, 'c': {'d': 1, 'e': 2, 'f': {'g': 1, 'h': 2}}}))
    print(script._call_func_pyobj_inout('echo', {'a': 1, 'b': 2, 'c': {'d': 1, 'e': 2, 'f': {'g': 1, 'h': 2, 'i': datetime.datetime.now()}}}))