from functools import lru_cache

from .helper_bridging import OSAObjProxy, DefaultOSAObjProxy, HelperScript

class Application(DefaultOSAObjProxy):
    def __init__(self, name: str, script: HelperScript = None):
        if script is None:
            self._helper_script = HelperScript.default
        else:
            self._helper_script = script
        self.obj_id = None
        response = self._helper_script.get_application(name)
        super().__init__(self._helper_script, response.obj_id, response.class_name)
        self._helper_script = self._helper_script.within_application(self)
        self._associsated_application = self

    @property
    def id(self) -> str:
        """The unique identifier of the application."""
        return self._call_method('id')
    
    @property
    def name(self) -> str:
        """The name of the application."""
        return self._call_method('name') # The name is a function so it needs special handling

    @property
    def frontmost(self):
        """Whether the application is currently frontmost."""
        return self._call_method('frontmost')

    def activate(self):
        """Activate the application."""
        return self._call_method('activate')

    @lru_cache(maxsize=64)
    def parent_of_class(self, name: str):
        """Get the parent of the application of the specified class."""
        return self._call_method('parentOfClass', args=[name])

class ApplicationExtension:
    def __init__(self, app: Application):
        self.app = app

    def eval_jxa_code_snippet(self, source: str, locals: dict = None):
        """Evaluate a JXA code piece."""
        if locals is None:
            locals = {}
        script = self.app.script
        payload = {
            'source': source,
            'locals': locals
        }
        payload = OSAObjProxy.pyobj_to_json( payload)
        return OSAObjProxy.json_to_pyobj(script, script.call_json('evalJXACodeSnippet', payload))
    
    def eval_applescript_code_snippet(self, source: str):
        """Evaluate an AppleScript code piece."""
        script = self.app.script
        payload = {
            'source': source,
        }
        payload = OSAObjProxy.pyobj_to_json(payload)
        return OSAObjProxy.json_to_pyobj(script, script.call_json('evalAppleScriptCodeSnippet', params=payload))
    