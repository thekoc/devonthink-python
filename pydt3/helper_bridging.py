from __future__ import annotations

import datetime
import json
import os
import logging

from typing import Optional, TYPE_CHECKING
from functools import lru_cache

from .osascript import OSAScript
from .objproxy import OSAObjProxy, OSAObjArray, DefaultOSAObjProxy


if TYPE_CHECKING:
    from Foundation import NSAppleScript
    from .application import Application


logger = logging.getLogger(__name__)

DEFAULT_SCRIPT_PATH = os.path.join(os.path.dirname(__file__), 'jxa_helper.scpt')


class HelperScript(OSAScript):
    _class_map = {} # type: dict[str, dict[str, type[OSAObjProxy]]]
    _default_app_class_map = {}

    default: HelperScript

    def __init__(self, script: NSAppleScript, osaobj_rc: Optional[dict] = None):
        super().__init__(script)
        self._osaobj_rc = {} if osaobj_rc is None else osaobj_rc

    def _unwrap_from_json(self, response: dict):
        if response['type'] == 'plain':
            return response.get('data')
        elif response['type'] == 'date':
            data = response.get('data')
            return datetime.datetime.fromtimestamp(data)
        elif response['type'] == 'reference':
            class_name = response.get('className', None)
            app_name = response.get('app', None)
            obj_id = response['objId']
            reference_cls = self.determine_class(app_name, class_name)
            logger.debug(f'determined reference_cls: {reference_cls}')
            assert issubclass(reference_cls, OSAObjProxy)
            proxy = reference_cls(helper_script=self, obj_id=obj_id, class_name=class_name)
            return proxy

        elif response['type'] == 'array':
            data = response['data']
            assert isinstance(data, list)
            return [
                self._unwrap_from_json(i) for i in data
            ]
        elif response['type'] == 'dict':
            data = response['data']
            assert isinstance(data, dict)
            return {
                k: self._unwrap_from_json(v) for k, v in data.items()
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
            if obj._helper_script is not self:
                raise ValueError('The proxy object is not created by this script')
            return {
                'type': 'reference',
                'objId': obj.obj_id
            }
        else:
            raise TypeError(f'Unsupported type: {type(obj)}')
    
    def _call_func_pyobj_inout(self, func_name: str, params):

        params = self._wrap_to_json(params)
        logger.debug(f'func_name: {func_name}')
        params = json.dumps(params)
        logger.debug(f'params: {params}')
        result = self._call_str(func_name, params)
        logger.debug(f'result: {result}')

        result = json.loads(result)
        return self._unwrap_from_json(result)


    def echo(self, params):
        return self._call_func_pyobj_inout('echo', params)
    
    def release_object_with_id(self, id: int):
        return self._call_func_pyobj_inout('releaseObjectWithId', {'id': id})

    def get_application(self, name: str) -> Application:
        return self._call_func_pyobj_inout('getApplication', {'name': name})
    
    def eval_jxa_code_snippet(self, source: str, locals: Optional[dict] = None):
        return self._call_func_pyobj_inout('evalJXACodeSnippet', {'source': source, 'locals': locals})
    
    def eval_applescript_code_snippet(self, source: str, locals: Optional[dict] = None):
        return self._call_func_pyobj_inout('evalAppleScriptCodeSnippet', {'source': source, 'locals': locals})

    def get_property(self, obj: OSAObjProxy, name: str):
        return self._call_func_pyobj_inout('getProperty', {'obj': obj, 'name': name})

    def get_properties(self, obj: OSAObjProxy, properties: list):
        return self._call_func_pyobj_inout('getProperties', {'obj': obj, 'properties': properties})

    def set_properties(self, obj: OSAObjProxy, key_values: dict):
        return self._call_func_pyobj_inout('setProperties', {'obj': obj, 'keyValues': key_values})
    
    def call_method(self, obj: OSAObjProxy, name: str, args = None, kwargs: dict = None):
        return self._call_func_pyobj_inout('callMethod', {'obj': obj, 'name': name, 'args': args, 'kwargs': kwargs})

    def call_self(self, obj: OSAObjProxy, args = None, kwargs: dict = None):
        return self._call_func_pyobj_inout('callSelf', {'obj': obj, 'args': args, 'kwargs': kwargs})

    def get_parent_of_class(self, application: str, class_name: str):
        return self.eval_jxa_code_snippet(f'Application("{application}").parentOfClass("{class_name}")')

    @lru_cache(maxsize=1024)
    def determine_class(self, app_name: str, class_name: str | None) -> type[OSAObjProxy]:
        if class_name is None:
            return DefaultOSAObjProxy
        elif class_name.startswith('array::'):
            return OSAObjArray
        elif class_name == 'function':
            return DefaultOSAObjProxy


        current_class_name = class_name
        reference_cls = None
        while current_class_name is not None:
            class_map = self._class_map.get(app_name, self._default_app_class_map)
            reference_cls = class_map.get(current_class_name)
            if reference_cls is not None:
                return reference_cls
            elif app_name is None:
                return DefaultOSAObjProxy
            else:
                current_class_name = self.get_parent_of_class(app_name, current_class_name)

        return DefaultOSAObjProxy

    @classmethod
    def register_class_map(cls, app_name: str, class_map: dict[str, type[OSAObjProxy]]):
        cls._class_map[app_name] = class_map
    
    @classmethod
    def set_default_class_map(cls, class_map: dict[str, type[OSAObjProxy]]):
        cls._default_app_class_map = class_map

    def __hash__(self) -> int:
        return id(self)


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