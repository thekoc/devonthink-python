import os

from .osascript import OSAScript, DefaultOSAObjProxy

SCRIPT_PATH = os.path.join(os.path.dirname(__file__), 'jxa_helper.scpt')


class Application(DefaultOSAObjProxy):
    def __init__(self, name) -> None:
        self.name = name
        self.script = OSAScript.from_path(SCRIPT_PATH)
        response = self.script.call_json('getApplication', {'name': self.name})
        super().__init__(self.script, response['objId'], response['className'])
