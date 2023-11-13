from ...helper_bridging import HelperScript


from .devonthink import DEVONthink3
from .database import Database
from .item import Item
from .record import Record
from .reminder import Reminder
from .smartgroup import SmartGroup
from .text import Text
from .windows import (ThinkWindow, DocumentWindow, ViewerWindow)


HelperScript._NAME_CLASS_MAP['database'] = Database
HelperScript._NAME_CLASS_MAP['item'] = Item
HelperScript._NAME_CLASS_MAP['record'] = Record
HelperScript._NAME_CLASS_MAP['reminder'] = Reminder
HelperScript._NAME_CLASS_MAP['text'] = Text
HelperScript._NAME_CLASS_MAP['smartGroup'] = SmartGroup

HelperScript._NAME_CLASS_MAP['thinkWindow'] = ThinkWindow
HelperScript._NAME_CLASS_MAP['documentWindow'] = DocumentWindow
HelperScript._NAME_CLASS_MAP['viewerWindow'] = ViewerWindow
