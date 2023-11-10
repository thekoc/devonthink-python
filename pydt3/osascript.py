from __future__ import annotations

import json
import os
from logging import getLogger
from Foundation import NSAppleScript, NSURL, NSAppleEventDescriptor


logger = getLogger(__name__)



DEFAULT_SCRIPT_PATH = os.path.join(os.path.dirname(__file__), 'jxa_helper.scpt')

class OSAScript:
    default: 'OSAScript'

    def __init__(self, script: NSAppleScript):
        self.script = script

    @classmethod
    def from_path(cls, path):
        url = NSURL.fileURLWithPath_(path)
        script, error = NSAppleScript.alloc().initWithContentsOfURL_error_(url, None)
        if error:
            raise RuntimeError(error)
        return cls(script)

    def _call_str(self, func_name: str, arg: str):
        script = self.script
        event = NSAppleEventDescriptor.appleEventWithEventClass_eventID_targetDescriptor_returnID_transactionID_(
            self.fourcharcode(b'ascr'), self.fourcharcode(b'psbr'), NSAppleEventDescriptor.nullDescriptor(), 0, 0)
        descriptor_list = NSAppleEventDescriptor.listDescriptor()
        descriptor_list.insertDescriptor_atIndex_(NSAppleEventDescriptor.descriptorWithString_(arg), 0)
        event.setDescriptor_forKeyword_(descriptor_list, self.fourcharcode(b'----'))

        event.setDescriptor_forKeyword_(NSAppleEventDescriptor.descriptorWithString_(func_name), self.fourcharcode(b'snam'))

        result, error = script.executeAppleEvent_error_(event, None)
        if error:
            raise RuntimeError(error)
        else:
            return result.stringValue()
    
    def call_json_io(self, func_name: str, params: dict):
        param_str = json.dumps(params)
        logger.debug(f'call_json_io func_name {func_name} params: {param_str}')
        result = self._call(func_name, param_str)
        logger.debug(f'call_json_io result: {result}')
        return json.loads(result)

    def fourcharcode(self, chars: bytes):
        return int.from_bytes(chars, 'big')

OSAScript.default = OSAScript.from_path(DEFAULT_SCRIPT_PATH)

if __name__ == '__main__':
    script = OSAScript.from_path('/Users/koc/Developer/devonthink/python-api/pydt3/test.scpt')
    print(script._call('echo', 'hello world'))