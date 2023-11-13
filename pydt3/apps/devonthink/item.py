
from ...osascript import OSAScript
from ...helper_bridging import OSAObjProxy

class Item(OSAObjProxy):
    def __init__(self, script: 'OSAScript', obj_id: int, class_name: str):
        super().__init__(script, obj_id, class_name)
