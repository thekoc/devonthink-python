
from ..osascript import OSAScript, OSAObjProxy

class Item(OSAObjProxy):
    def __init__(self, script: 'OSAScript', obj_id: int, class_name: str):
        super().__init__(script, obj_id, class_name)
        

OSAObjProxy._NAME_CLASS_MAP['item'] = Item