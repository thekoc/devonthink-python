from __future__ import annotations

from typing import Optional, Union, List, TYPE_CHECKING

from ...application import Application
from ...helper_bridging import HelperScript
from ...helper_bridging import OSAObjArray

if TYPE_CHECKING:
    from .record import Record
    from .database import Database
    from .windows import (ThinkWindow, DocumentWindow, ViewerWindow)


class DEVONthink3(Application):
    def __init__(self, helper_script: Optional[HelperScript] = None, obj_id: Optional[int] = None, class_name: Optional[str] = None):
        super().__init__('DEVONthink 3', helper_script, obj_id, class_name)
        self._ext = DevonthinkExtension(self)

    @property
    def ext(self) -> 'DevonthinkExtension':
        """Extension methods for DEVONthink 3. These methods are not part of the DEVONthink's AppleScript API.

        Examples:
            >>> dtp3 = DEVONthink3()
            >>> dtp3.ext.db_by_name('blue-book')
        Returns:
            DevonthinkExtension
        """
        return self._ext
    
    @classmethod
    def from_script(cls, script: HelperScript) -> DEVONthink3:
        return script.get_application("DEVONthink 3")
    
    # elements
    @property
    def databases(self) -> OSAObjArray[Database]:
        return self._get_property('databases')
    
    @property
    def document_windows(self) -> OSAObjArray[DocumentWindow]:
        return self._get_property('documentWindows')

    @property
    def selected_records(self) -> OSAObjArray[Record]:
        return self._get_property('selectedRecords')
    
    @property
    def think_windows(self) -> OSAObjArray[ThinkWindow]:
        return self._get_property('thinkWindows')

    @property
    def viewer_windows(self) -> OSAObjArray[ViewerWindow]:
        return self._get_property('viewerWindows')

    # properties
    @property
    def bates_number(self) -> int:
        """Current bates number."""
        return self._call_method('batesNumber')

    @property
    def cancelled_progress(self) -> bool:
        """Specifies if a process with visible progress indicator should be cancelled."""
        return self._call_method('cancelledProgress')

    @property
    def content_record(self) -> Record:
        """The record of the visible document in the frontmost think window."""
        return self._get_property('contentRecord')

    @property
    def current_database(self) -> Database:
        """The currently used database."""
        return self._get_property('currentDatabase')

    @property
    def current_group(self) -> Record:
        """The (selected) group of the frontmost window of the current database. Returns root of current database if no current group exists."""
        return self._get_property('currentGroup')

    @property
    def current_workspace(self) -> Optional[str]:
        """The name of the currently used workspace."""
        return self._call_method('currentWorkspace')

    @property
    def inbox(self) -> Database:
        """The global inbox."""
        return self._get_property('inbox')

    @property
    def incoming_group(self) -> Record:
        """The default group for new notes. Either global inbox or incoming group of current database if global inbox isn't available."""
        return self._get_property('incomingGroup')

    @property
    def last_downloaded_URL(self) -> str:
        """The actual URL of the last download."""
        return self._call_method('lastDownloadedURL')

    @property
    def last_downloaded_response(self) -> Optional[Record]:
        """HTTP-Status, Last-Modified, Content-Type, Content-Length and Charset of last HTTP(S) response."""
        return self._call_method('lastDownloadedResponse')

    @property
    def preferred_import_destination(self) -> Record:
        """The default destination for data from external sources. See Preferences > Import > Destination."""
        return self._get_property('preferredImportDestination')

    @property
    def reading_list(self) -> List[dict]:
        """The items of the reading list."""
        return self._call_method('readingList')

    @property
    def selection(self) -> list:
        """Not implemented due to the poor document. Plus it's 
        officially not recommanded:

            selection (list, r/o) : The current selection of
            the frontmost viewer window or the record of the
            frontmost document window. 'selected records'
            relationship is recommended instead especially for
            bulk retrieval of properties like UUID.

        """
        raise NotImplementedError()

    @property
    def workspaces(self) -> List[str]:
        """The names of all available workspaces."""
        return self._call_method('workspaces')
    
    # methods
    ## standard additions
    def display_dialog(self, text: str, place_holder: str = None, buttons: List[str]=None, default_button: str = None, with_icon: str = None) -> str:
        """Display a dialog.

        Args:
            text (str): The text to display.
            place_holder (str): The placeholder text.
            with_icon (str): The icon to display.
            buttons (List[str]): The buttons to display.
            default_button (str): The default button.

        Returns:
            str: The selected button.
        """
        kwargs = {
            'defaultAnswer': place_holder,
            'buttons': buttons,
            'defaultButton': default_button,
            'withIcon': with_icon,
        }

        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        return self._call_method('displayDialog', [text], kwargs)
    
    
    def display_notification(self, text: str, with_title: str = None, subtitle: str = None, sound_name: str = None) -> None:
        return self._call_method('displayNotification', [text], {
            'withTitle': with_title,
            'subtitle': subtitle,
            'soundName': sound_name,
        })
    
    
    # DEVONthink suit

    def show_progress_indicator(self, title: str, cancel_button: bool, steps: int) -> bool:
        """Show a progress indicator or update an already visible indicator. You have to ensure that the indicator is hidden again via 'hide progress indicator' when the script ends or if an error occurs.
        
        Args:
            title (str): The title of the progress.
            cancel_button (bool):  Display a button to cancel the process.
            steps (int):  The number of steps of the progress or a negative value for an indeterminate number.
        """
        return self._call_method('showProgressIndicator', [title], {
            'cancelButton': cancel_button,
            'steps': steps,
        })
    
    def hide_progress_indicator(self) -> bool:
        """Hide a visible progress indicator."""
        return self._call_method('hideProgressIndicator')
        
    def step_progress_indicator(self, title) -> bool:
        """Go to next step of a progress."""
        return self._call_method('stepProgressIndicator', [title])

    def search(self, text: str, comparision: str = 'no case', excludeSubgroups: bool = False) -> OSAObjArray[Record]:
        """Search for records in specified group or all databases.

        Args:
            text (str): The search string.
            comparision (str, optional):  The comparison to use (default `'no case'`). One of fuzzy/‌no case/‌no umlauts.
            excludeSubgroups (bool, optional): Don't search in subgroups of the specified group. (default `false`).

        Returns:
            List[Record]: The list of records matching the search string.
        """
        return self._call_method('search', [text], {
            'comparision': comparision,
            'excludeSubgroups': excludeSubgroups,
        })

    def import_(self, file_path: str, source_app: str = None, record_name: str = None, placeholders: dict = None, to: Record = None) -> Record:
        """Import a file or folder (including its subfolders).

        Args:
            file_path (str): The POSIX path of the file or folder.
            source_app (str, optional): The name of the source application. Default is None.
            record_name (str, optional): The name for the imported record. Default is None.
            placeholders (dict, optional): Optional placeholders as key-value-pairs for text, RTF/RTFD & HTML/XML templates and filenames. Default is None.
            to (Group, optional): he destination group. Uses incoming group or group selector if not specified. Default is None.

        Returns:
            Record: The imported record.
        """
        return self._call_method('import', [file_path], {
            'from': source_app,
            'name': record_name,
            'placeholders': placeholders,
            'to': to,
        })

    def indicate(self, text: str, to_: Optional[Record] = None, file_type: Optional[int] = None) -> Record:
        """Indicate ('index') a file or folder (including its subfolders). If no type is specified or the type is 'all', then links to unknown file types are created too.

        Args:
            text (str): The POSIX path of the file or folder.
            dest (Record, optional): The destination group. Uses incoming group or group selector if not specified.
            file_type (int, optional): Obsolete.

        Returns:
            Record: The record of the indicated file or folder.
        """
        return self._call_method('indicate', text, {
            'to': to_,
            'fileType': file_type,
        })

    def index(self, text: str, to_: Optional[Record] = None, file_type: Optional[int] = None) -> Record:
        """Alias for `indicate`."""
        return self.indicate(text, to_, file_type)

    def open_database(self, file_path: str) -> Database:
        """Open an existing database.

        Args:
            file_path (str): The POSIX file path of the database.

        Returns:
            Database: The opened database.
        """
        return self._call_method('open database', [file_path])
    
    def create_database(self, path: str) -> Database:
        """Create a new database.

        Args:
            text (str): POSIX file path of database.

        Returns:
            Database: The new database object.
        """
        return self._call_method('createDatabase', [path])

    def create_location(self, path: str, database: Database = None) -> Record:
        """Create a hierarchy of groups if necessary.

        Args:
            path (str): The hierarchy as a POSIX path (/ in names has to be replaced with \/, see location property).
            database (Database, optional): The database. Uses current database if not specified.

        Returns:
            Record: The created record.
        """
        return self._call_method('createLocation', [path], {
            'in': database,
        })

    def create_record_with(self, properties: dict, in_: Optional['Record'] = None) -> Record:
        """Create a new record.

        Args:
            record (dict): The properties of the record. Possible keys for record are 'name', 'type', 'comment', 'path', 'URL', 'creation date', 'modification date', 'date', 'plain text', 'rich text', 'source', 'data', 'content', 'columns', 'cells', 'thumbnail' and 'tags'.
            in_ (Record, optional): The destination group for the new record. Uses incoming group or group selector if not specified.
        Returns:
            Record: The newly created record.
        """
        return self._call_method('createRecordWith', [properties], {'in': in_})

    def delete(self, record: 'Record', in_: Optional['Record'] = None) -> bool:
        """Delete all instances of a record from the database or one instance from the specified group.

        Args:
            record (Record): The record to delete.
            in_ (Record, optional): The parent group of this instance. Deletes all instances of the record from the database if not specified.

        Returns:
            bool: `True` if the deletion was successful.
        """
        return self._call_method('delete', [], {'record': record, 'in': in_})

    def get_database_with_uuid(self, text: str) -> Database:
        """Get database with the specified uuid.

        Args:
            text (str): The unique identifier.

        Returns:
            Database: The database with the specified uuid.
        """
        return self._call_method('getDatabaseWithUuid', [text])



    def move(self, record: Union[Record, List[Record]], to: Record, from_: Record = None) -> Union[Record, List[Record]]:
        """Move all instances of a record to a different group. Specify the "from" group to to move a single instance to a different group.

        Args:
            record (Union[Record, List[Record]]): The record or a list of records to move.
            to (Record): The destination group which doesn't have to be in the same database.
            from_ (Record, optional): The source group. Only applicable if record and destination group are in the same database.

        Returns:
            Union[Record, List[Record]]: The moved record or list of records.
        """
        return self._call_method('move', [], {
            'record': record,
            'to': to,
            'from': from_,
        })


    def replicate(self, record: Record, to: Record) -> Record:
        """Replicate a record.

        Args:
            record (Record): The record to replicate.
            to (Record): The destination group which must be in the same database.

        Returns:
            Record: The replicated record.
        """
        return self._call_method('replicate', [], {
            'record': record,
            'to': to,
        })

    def get_record_at(self, text: str, database: Optional[Database] = None) -> Record:
        """Search for record at the specified location.

        Args:
            text (str): The location of the record as a POSIX path (/ in names has to be replaced with \/, see location property).
            database (Database, optional): The database. Uses current database if not specified.

        Returns:
            Record: The record at the specified location.
        """
        return self._call_method('getRecordAt', [text], {'in': database})

    def get_record_with_uuid(self, text: str, database: Optional[Database] = None) -> Record:
        """Get record with the specified uuid or item link.

        Args:
            text (str): The unique identifier or item link.
            database (Database, optional): The database. Uses all databases if not specified.

        Returns:
            Record: The record with the specified uuid or item link.
        """
        return self._call_method('getRecordWithUuid', [text], {'in': database})
    
    def add_custom_meta_data(self, value, for_: str, to: Record):
        """Add user-defined metadata to a record. Setting a value for an unknown key automatically adds a definition to Preferences > Data.

           Note that space cannot present in the key's name when adding a new key.
           This is the limitation set by DEVONthink itself. You should add names
           with spaces directly in DEVONthink's GUI.

           More details: https://discourse.devontechnologies.com/t/how-to-modify-a-custom-field-value-using-applescript/64384/10

        Args:
            value (Any): The value to add.
            for_ (str): The key for the user-defined value.
            to (Record): The record.
        """
        return self._call_method('addCustomMetaData', [value], {'for': for_, 'to': to})

    def open_tab_for(self, in_think_window: ThinkWindow = None, record: Record = None, referrer: str = None, url: str = None) -> Tab:
        """Open a new tab for the specified URL or record in a think window.

        Args:
            in_think_window (ThinkWindow, optional): The think window that should open a new tab. A new window is used otherwise.
            record (Record, optional): The record to open.
            referrer (str, optional): The HTTP referrer.
            url (str, optional): The URL to open.

        Returns:
            Tab: The newly opened tab.
        """
        kwargs = {}
        if in_think_window is not None:
            kwargs['in'] = in_think_window
        if record is not None:
            kwargs['record'] = record
        if referrer is not None:
            kwargs['referrer'] = referrer
        if url is not None:
            kwargs['url'] = url
        return self._call_method('openTabFor', args=None, kwargs=kwargs)

    def open_window_for(self, record: Record, force: bool = False) -> ThinkWindow:
        """Open a (new) viewer or document window for the specified record (use the 'close' command to close a window). Only recommended for viewer windows, use 'open tab for' for document windows.

        Args:
            record (Record): The record to open.
            force (bool, optional): Force DEVONthink to always open a new window, even if the record is already opened in one. Off by default.

        Returns:
            ThinkWindow: The newly opened think window.
        """
        return self._call_method('openWindowFor', kwargs={'record': record, 'force': force})

    def get_custom_meta_data(self, for_: str, from_: Record, default_value=None):
        """Get user-defined metadata from a record.

        Args:
            for_ (str): The key of the user-defined value.
            from_ (Record): The record.
            default_value (_type_, optional): Default value if user-defined metadata does not yet exist, otherwise a missing value is returned. Defaults to None.
        """
        payload = {
            'for': for_,
            'from': from_,
        }

        if default_value is not None:
            payload['default_value'] = default_value
        return self._call_method('getCustomMetaData', [], payload)
    
    def __repr__(self):
        return f'<DEVONthink3 {self.id}>'

class DevonthinkExtension():
    def __init__(self, app: DEVONthink3):
        self.app = app
    
    def db_by_name(self, name: str) -> Optional[Database]:
        dbs = self.app.databases
        for db in dbs:
            if db.name == name:
                return db