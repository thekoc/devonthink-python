from ...helper_bridging import HelperScript


from .devonthink import DEVONthink3
from .database import Database
from .item import Item
from .record import Record
from .reminder import Reminder
from .smartgroup import SmartGroup
from .text import Text
from .windows import (ThinkWindow, DocumentWindow, ViewerWindow)

HelperScript.register_class_map(app_name='DEVONthink 3', class_map={
    'application': DEVONthink3,
    'database': Database,
    'item': Item,
    'record': Record,
    'reminder': Reminder,
    'text': Text,
    'smartGroup': SmartGroup,
    'thinkWindow': ThinkWindow,
    'documentWindow': DocumentWindow,
    'viewerWindow': ViewerWindow
})
