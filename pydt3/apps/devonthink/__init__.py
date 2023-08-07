from ...osascript import OSAObjProxy


from .devonthink import DEVONthink3
from .database import Database
from .item import Item
from .record import Record
from .reminder import Reminder
from .smartgroup import SmartGroup
from .text import Text
from .windows import (ThinkWindow, DocumentWindow, ViewerWindow)


OSAObjProxy._NAME_CLASS_MAP['database'] = Database
OSAObjProxy._NAME_CLASS_MAP['item'] = Item
OSAObjProxy._NAME_CLASS_MAP['record'] = Record
OSAObjProxy._NAME_CLASS_MAP['reminder'] = Reminder
OSAObjProxy._NAME_CLASS_MAP['text'] = Text
OSAObjProxy._NAME_CLASS_MAP['smartGroup'] = SmartGroup

OSAObjProxy._NAME_CLASS_MAP['thinkWindow'] = ThinkWindow
OSAObjProxy._NAME_CLASS_MAP['documentWindow'] = DocumentWindow
OSAObjProxy._NAME_CLASS_MAP['viewerWindow'] = ViewerWindow
