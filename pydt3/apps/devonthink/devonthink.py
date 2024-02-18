from __future__ import annotations

from typing import Optional, Union, Any, List, TYPE_CHECKING

from ...application import Application
from ...helper_bridging import HelperScript
from ...helper_bridging import OSAObjArray, OSAObjProxy

if TYPE_CHECKING:
    from .record import Record
    from .database import Database
    from .windows import (ThinkWindow, DocumentWindow, ViewerWindow)
    from .tab import Tab


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

    def add_download(self, url: str, automatic: bool = False, password: str = None, referrer: str = None, user: str = None) -> bool:
        """Add a URL to the download manager.
        
        Args:
            url (str): The URL to add.
            automatic (bool, optional): Automatic or user (default) download. Defaults to False.
            password (str, optional): The password for protected websites.
            referrer (str, optional): The HTTP referrer.
            user (str, optional): The user name for protected websites.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        kwargs = {
            'automatic': automatic,
            'password': password,
            'referrer': referrer,
            'user': user
        }
        return self._call_method('addDownload', args=[url], kwargs={k: v for k, v in kwargs.items() if v is not None})

    def add_reading_list(self, record: Record = None, title: str = None, url: str = None) -> bool:
        """Add record or URL to reading list.
        
        Args:
            record (Record, optional): The record. Only documents are supported.
            title (str, optional): The title of the webpage.
            url (str, optional): The URL of the webpage.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        kwargs = {
            'record': record,
            'title': title,
            'url': url
        }
        return self._call_method('addReadingList', args=None, kwargs={k: v for k, v in kwargs.items() if v is not None})

    def add_row(self, specifier, cells: list = None) -> bool:
        """Add new row to current sheet.
        
        Args:
            specifier: The object for the command.
            cells (list, optional): Cells of new row.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        kwargs = {
            'cells': cells
        }
        return self._call_method('addRow', args=[specifier], kwargs={k: v for k, v in kwargs.items() if v is not None})

    def check_file_integrity_of(self, database: Database) -> int:
        """Check file integrity of database. Returns number of files having an invalid content hash.
        
        Args:
            database (Database): The database to check.
        
        Returns:
            int: Number of files having an invalid content hash.
        """
        return self._call_method('checkFileIntegrityOf', args=None, kwargs={'database': database})

    def classify(self, record: Record, comparison: str = "data comparison", in_db: Database = None) -> list:
        """Get a list of classification proposals.
        
        Args:
            record (Record): The record to classify.
            comparison (str, optional): The comparison to use (default is "data comparison").
            in_db (Database, optional): The database. Uses all databases if not specified.
        
        Returns:
            list: A list of classification proposals.
        """
        kwargs = {
            'record': record,
            'comparison': comparison,
            'in': in_db
        }
        return self._call_method('classify', args=None, kwargs={k: v for k, v in kwargs.items() if v is not None})

    def compare(self, comparison: str = "data comparison", content: str = None, record: Record = None, to: Database = None) -> list:
        """Get a list of similar records, either by specifying a record or a content.
        
        Args:
            comparison (str, optional): The comparison to use (default is "data comparison").
            content (str, optional): The content to compare.
            record (Record, optional): The record to compare.
            to (Database, optional): The database. Uses all databases if not specified.
        
        Returns:
            list: A list of similar records.
        """
        kwargs = {
            'comparison': comparison,
            'content': content,
            'record': record,
            'to': to
        }
        return self._call_method('compare', args=None, kwargs={k: v for k, v in kwargs.items() if v is not None})

    def compress(self, database: Database, to: str) -> bool:
        """Compress a database into a Zip archive.
        
        Args:
            database (Database): The database to compress.
            to (str): POSIX path of Zip archive.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        return self._call_method('compress', args=None, kwargs={'database': database, 'to': to})

    def consolidate(self, record: Record) -> bool:
        """Move an external/indexed record (and its children) into the database.

        Args:
            record (Record): The record to consolidate.

        Returns:
            bool: True if successful, False otherwise.
        """
        return self._call_method('consolidate', args=None, kwargs={'record': record})

    def convert(self, record: Record, in_group: Record = None, to: str = "simple") -> Record:
        """Convert a record to plain or rich text, formatted note or HTML and create a new record afterwards.

        Args:
            record (Record): The record or a list of records to convert.
            in_group (Record, optional): The destination group for the converted record. Parents of the record to convert are used if not specified.
            to (str, optional): The desired format. Defaults to "simple".

        Returns:
            Record: The converted record.
        """
        kwargs = {
            'record': record,
            'in': in_group,
            'to': to
        }
        return self._call_method('convert', args=None, kwargs={k: v for k, v in kwargs.items() if v is not None})

    def convert_feed_to_html(self, text: str, base_url: str = None) -> str:
        """Convert a RSS, RDF, or Atom feed to HTML.
        
        Args:
            text (str): The source code of the feed.
            base_url (str, optional): The URL of the feed.
        
        Returns:
            str: The converted HTML text.
        """
        kwargs = {
            'baseURL': base_url
        }
        return self._call_method('convertFeedToHTML', args=[text], kwargs={k: v for k, v in kwargs.items() if v is not None})

    def create_database(self, text: str) -> Database:
        """Create a new database.
        
        Args:
            text (str): POSIX file path of database.
        
        Returns:
            Database: The created database object.
        """
        return self._call_method('createDatabase', args=[text], kwargs={})

    def create_formatted_note_from(self, text: str, agent: str = None, in_: Record = None, name: str = None, readability: bool = None, referrer: str = None, source: str = None) -> Record:
        """Create a new formatted note from a web page.
        
        Args:
            text (str): The URL to download.
            agent (str, optional): The user agent.
            in_ (Record, optional): The destination group for the new record. Uses incoming group or group selector if not specified.
            name (str, optional): The name for the new record.
            readability (bool, optional): Declutter page layout.
            referrer (str, optional): The HTTP referrer.
            source (str, optional): The HTML source.
        
        Returns:
            Record: The new record created.
        """
        kwargs = {
            'agent': agent,
            'in': in_,
            'name': name,
            'readability': readability,
            'referrer': referrer,
            'source': source
        }
        return self._call_method('createFormattedNoteFrom', args=[text], kwargs={k: v for k, v in kwargs.items() if v is not None})

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

    def create_markdown_from(self, url: str, agent: str = None, in_: Record = None, name: str = None, readability: bool = None, referrer: str = None) -> Record:
        """Create a Markdown document from a web resource.

        Args:
            url (str): The URL to download.
            agent (str, optional): The user agent.
            in_ (Record, optional): The destination group for the new record. Uses incoming group or group selector if not specified.
            name (str, optional): The name for the new record.
            readability (bool, optional): Declutter page layout.
            referrer (str, optional): The HTTP referrer.

        Returns:
            Record: The new record.
        """
        kwargs = {
            'agent': agent,
            'in': in_,
            'name': name,
            'readability': readability,
            'referrer': referrer
        }
        return self._call_method('createMarkdownFrom', args=[url], kwargs={k: v for k, v in kwargs.items() if v is not None})

    def create_pdf_document_from(self, url: str, agent: str = None, destination_group: Record = None, name: str = None, pagination: bool = None, readability: bool = None, referrer: str = None, width: int = None) -> Record:
        """Create a new PDF document with or without pagination from a web resource.

        Args:
            url (str): The URL to download.
            agent (str, optional): The user agent.
            destination_group (Record, optional): The destination group for the new record. Uses incoming group or group selector if not specified.
            name (str, optional): The name for the new record.
            pagination (bool, optional): Paginate PDF document or not.
            readability (bool, optional): Declutter page layout.
            referrer (str, optional): The HTTP referrer.
            width (int, optional): The preferred width for the PDF document in pixels.

        Returns:
            Record: The new PDF document record.
        """
        kwargs = {
            'agent': agent,
            'in': destination_group,
            'name': name,
            'pagination': pagination,
            'readability': readability,
            'referrer': referrer,
            'width': width
        }
        return self._call_method('createPDFDocumentFrom', args=[url], kwargs={k: v for k, v in kwargs.items() if v is not None})

    def create_record_with(self, properties: dict, in_: Optional['Record'] = None) -> Record:
        """Create a new record.

        Args:
            record (dict): The properties of the record. Possible keys for record are 'name', 'type', 'comment', 'path', 'URL', 'creation date', 'modification date', 'date', 'plain text', 'rich text', 'source', 'data', 'content', 'columns', 'cells', 'thumbnail' and 'tags'.
            in_ (Record, optional): The destination group for the new record. Uses incoming group or group selector if not specified.
        Returns:
            Record: The newly created record.
        """
        return self._call_method('createRecordWith', [properties], {'in': in_})

    def create_thumbnail(self, for_record: Record) -> bool:
        """Create or update existing thumbnail of a record. Thumbnailing is performed asynchronously in the background.
        
        Args:
            for_record (Record): The record.
        
        Returns:
            bool: True if successful, False otherwise.
        """

        return self._call_method('createThumbnail', args=None, kwargs={'for': for_record})

    def create_web_document_from(self, url: str, agent: str = None, in_record: Record = None, name: str = None, readability: bool = None, referrer: str = None) -> Record:
        """Create a new record (picture, PDF, or web archive) from a web resource.

        Args:
            url (str): The URL to download.
            agent (str, optional): The user agent.
            in_record (Record, optional): The destination group for the new record. Uses incoming group or group selector if not specified.
            name (str, optional): The name for the new record.
            readability (bool, optional): Declutter page layout.
            referrer (str, optional): The HTTP referrer.

        Returns:
            Record: The newly created record.
        """
        kwargs = {
            'agent': agent,
            'in': in_record,
            'name': name,
            'readability': readability,
            'referrer': referrer
        }
        return self._call_method('createWebDocumentFrom', args=[url], kwargs={k: v for k, v in kwargs.items() if v is not None})

    def deconsolidate(self, record: Record, to: str = None) -> bool:
        """Move an internal/imported record (and its children) to the enclosing external folder in the filesystem. Creation/Modification dates, Spotlight comments and OpenMeta tags are immediately updated.
        
        Args:
            record (Record): The record to deconsolidate.
            to (str, optional): The POSIX path of the destination folder. Only supported by documents.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        kwargs = {
            'record': record,
            'to': to
        }
        return self._call_method('deconsolidate', args=None, kwargs={k: v for k, v in kwargs.items() if v is not None})

    def delete(self, record: 'Record', in_: Optional['Record'] = None) -> bool:
        """Delete all instances of a record from the database or one instance from the specified group.

        Args:
            record (Record): The record to delete.
            in_ (Record, optional): The parent group of this instance. Deletes all instances of the record from the database if not specified.

        Returns:
            bool: `True` if the deletion was successful.
        """
        return self._call_method('delete', [], {'record': record, 'in': in_})

    def delete_row_at(self, specifier, *, position: int) -> bool:
        """Remove row at specified position from current sheet.
        
        Args:
            specifier: The object for the command.
            position (int): Position of the row (1...n).
        
        Returns:
            bool: True if successful, False otherwise.
        """
        return self._call_method('deleteRowAt', args=[specifier], kwargs={'position': position})

    def delete_thumbnail(self, of: Record) -> bool:
        """Delete existing thumbnail of a record.
        
        Args:
            of (Record): The record.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        return self._call_method('deleteThumbnail', kwargs={'of': of})

    def delete_workspace(self, name: str) -> bool:
        """Delete a workspace.

        Args:
            name (str): The name of the workspace.

        Returns:
            bool: True if successful, False otherwise.
        """
        return self._call_method('deleteWorkspace', args=[name])

    def display_authentication_dialog(self, text: str = None) -> dict:
        """Display a dialog to enter a username and its password.

        Args:
            text (str, optional): The info for the dialog.

        Returns:
            dict: A record containing the result.
        """
        args = [text] if text is not None else []
        return self._call_method('displayAuthenticationDialog', args=args)

    def display_group_selector(self, title: str, buttons: list = None, for_database: Database = None, name: bool = None, tags: bool = None) -> Any:
        """Display a dialog to select a (destination) group. Returns either the selected group (without name and tags parameters) due to compatibility to older versions or a dictionary containing the key-value pairs "group" and optionally "name" and "tags".
        
        Args:
            title (str): The title of the dialog.
            buttons (list, optional): The labels for the cancel and select buttons.
            for_database (Database, optional): The database. All open databases are used if not specified.
            name (bool, optional): Show field to enter a name (off by default).
            tags (bool, optional): Show field to enter tags (off by default).
        
        Returns:
            Any: The selected group or a dictionary containing the "group" and optionally "name" and "tags".
        """
        kwargs = {
            'buttons': buttons,
            'for': for_database,
            'name': name,
            'tags': tags
        }
        return self._call_method('displayGroupSelector', args=[title], kwargs={k: v for k, v in kwargs.items() if v is not None})

    def display_name_editor(self, title: str = None, default_answer: str = None, info: str = None) -> str:
        """Display a dialog to enter a name.

        Args:
            title (str, optional): The title of the dialog. By default, the application name.
            default_answer (str, optional): The default editable name.
            info (str, optional): The info for the dialog.

        Returns:
            str: The entered name.
        """
        args = [title] if title is not None else []
        kwargs = {
            'defaultAnswer': default_answer,
            'info': info
        }
        return self._call_method('displayNameEditor', args=args, kwargs={k: v for k, v in kwargs.items() if v is not None})

    def do_javascript(self, code: str, in_think_window: ThinkWindow = None) -> str:
        """Executes a string of JavaScript code (optionally in the web view of a think window).
        
        Args:
            code (str): The JavaScript code to execute.
            in_think_window (ThinkWindow, optional): The think window that the JavaScript should be executed in.
        
        Returns:
            str: The result of the JavaScript execution.
        """
        kwargs = {
            'in': in_think_window
        }
        return self._call_method('doJavaScript', args=[code], kwargs={k: v for k, v in kwargs.items() if v is not None})

    def download_json_from(self, url: str, agent: str = None, method: str = None, password: str = None, post: dict = None, referrer: str = None, user: str = None) -> dict:
        """Download a JSON object.

        Args:
            url (str): The URL of the JSON object to download.
            agent (str, optional): The user agent.
            method (str, optional): The HTTP method ("GET" by default).
            password (str, optional): The password for protected websites.
            post (dict, optional): A dictionary containing key-value pairs for HTTP POST actions.
            referrer (str, optional): The HTTP referrer.
            user (str, optional): The user name for protected websites.

        Returns:
            dict: The downloaded JSON object.
        """
        kwargs = {
            'agent': agent,
            'method': method,
            'password': password,
            'post': post,
            'referrer': referrer,
            'user': user
        }
        return self._call_method('downloadJSONFrom', args=[url], kwargs={k: v for k, v in kwargs.items() if v is not None})

    def download_markup_from(self, url: str, agent: str = None, encoding: str = None, method: str = None, password: str = None, post: dict = None, referrer: str = None, user: str = None) -> str:
        """Download an HTML or XML page (including RSS, RDF or Atom feeds).
        
        Args:
            url (str): The URL of the HTML or XML page to download.
            agent (str, optional): The user agent.
            encoding (str, optional): The encoding of the page (default ISO-Latin-1).
            method (str, optional): The HTTP method ("GET" by default).
            password (str, optional): The password for protected websites.
            post (dict, optional): A dictionary containing key-value pairs for HTTP POST actions.
            referrer (str, optional): The HTTP referrer.
            user (str, optional): The user name for protected websites.
        
        Returns:
            str: The downloaded markup text.
        """
        kwargs = {
            'agent': agent,
            'encoding': encoding,
            'method': method,
            'password': password,
            'post': post,
            'referrer': referrer,
            'user': user
        }
        return self._call_method('downloadMarkupFrom', args=[url], kwargs={k: v for k, v in kwargs.items() if v is not None})

    def duplicate(self, record: Record, to: Record) -> Record:
        """Duplicate a record or a list of records.
        
        Args:
            record (Record): The record or a list of records to duplicate.
            to (Record): The destination group which doesn't have to be in the same database.
        
        Returns:
            Record: The duplicated record or records.
        """
        kwargs = {
            'record': record,
            'to': to
        }
        return self._call_method('duplicate', args=None, kwargs=kwargs)

    def exists_record_at(self, path: str, database: Database = None) -> bool:
        """Check if at least one record exists at the specified location.

        Args:
            path (str): The location of the record as a POSIX path (/ in names has to be replaced with \/, see location property).
            database (Database, optional): The database. Uses current database if not specified.

        Returns:
            bool: True if at least one record exists, False otherwise.
        """
        return self._call_method('existsRecordAt', [path], {
            'in': database,
        })

    def exists_record_with_comment(self, comment: str, database: Database = None) -> bool:
        """Check if at least one record with the specified comment exists.

        Args:
            comment (str): The comment.
            database (Database, optional): The database. Uses current database if not specified.

        Returns:
            bool: True if at least one record exists, False otherwise.
        """
        return self._call_method('existsRecordWithComment', [comment], {
            'in': database,
        })

    def exists_record_with_path(self, path: str, database: Database = None) -> bool:
        """Check if at least one record with the specified path exists.

        Args:
            path (str): The path.
            database (Database, optional): The database. Uses current database if not specified.

        Returns:
            bool: True if at least one record exists, False otherwise.
        """
        return self._call_method('existsRecordWithPath', [path], {
            'in': database,
        })

    def export(self, record: Record, to: str) -> str:
        """Export a record (and its children).

        Args:
            record (Record): The record to export.
            to (str): The destination directory as a POSIX path. DEVONthink creates the destination if necessary.

        Returns:
            str: The path of the exported record.
        """
        return self._call_method('export', args=None, kwargs={'record': record, 'to': to})

    def export_tags_of(self, record: Record) -> bool:
        """Export Finder tags of a record.

        Args:
            record (Record): The record.

        Returns:
            bool: True if successful, False otherwise.
        """
        return self._call_method('exportTagsOf', args=None, kwargs={'record': record})

    def export_website(self, record: Record, to: str, encoding: str = None, entities: bool = None, index_pages: bool = None, template: str = None) -> str:
        """Export a record (and its children) as a website.

        Args:
            record (Record): The record to export.
            to (str): The destination directory as a POSIX path. DEVONthink creates the destination if necessary.
            encoding (str, optional): The encoding of the exported HTML pages (default ISO-Latin-1).
            entities (bool, optional): Use HTML entities. Off by default.
            index_pages (bool, optional): Create index pages. Off by default.
            template (str, optional): Name of built-in template or full POSIX path of template. Uses Default template if not specified.

        Returns:
            str: The path of the exported website.
        """
        kwargs = {
            'record': record,
            'to': to,
            'encoding': encoding,
            'entities': entities,
            'indexPages': index_pages,
            'template': template
        }
        return self._call_method('exportWebsite', args=None, kwargs={k: v for k, v in kwargs.items() if v is not None})

    def extract_keywords_from(self, record: Record, barcodes: bool = False, existing_tags: bool = False, hash_tags: bool = False, image_tags: bool = False) -> list:
        """Extract list of keywords from a record. The list is sorted by number of occurrences.

        Args:
            record (Record): The record.
            barcodes (bool, optional): Include scanned barcodes.
            existing_tags (bool, optional): Include existing tags (and their aliases) found in the title or text of the record.
            hash_tags (bool, optional): Include hash tags found in the title or text of the record.
            image_tags (bool, optional): Include suggested image tags.

        Returns:
            list: Sorted list of keywords.
        """
        kwargs = {
            'record': record,
            'barcodes': barcodes,
            'existingTags': existing_tags,
            'hashTags': hash_tags,
            'imageTags': image_tags
        }
        return self._call_method('extractKeywordsFrom', args=None, kwargs={k: v for k, v in kwargs.items() if v is not None})

    def get_cached_data_for_url(self, url: str, from_tab: Tab = None) -> Any:
        """Get cached data for URL of a resource which is part of a loaded webpage and its DOM tree, rendered in a think tab/window.

        Args:
            url (str): The URL.
            from_tab (Tab, optional): The source think tab. Uses current tab of frontmost think window otherwise.

        Returns:
            Any: The cached data.
        """
        kwargs = {
            'from': from_tab
        }
        return self._call_method('getCachedDataForURL', args=[url], kwargs={k: v for k, v in kwargs.items() if v is not None})

    def get_cell_at(self, specifier: OSAObjProxy, column: int, row: int) -> str:
        """Get content of cell at specified position of current sheet.

        Args:
            specifier: The object for the command.
            column (int): Either the index (1...n) or the name of the column of the cell.
            row (int): The row (1...n) of the cell.

        Returns:
            str: The content of the specified cell.
        """
        return self._call_method('getCellAt', args=[specifier], kwargs={'column': column, 'row': row})

    def get_concordance_of(self, record: Record, sorted_by: str = "weight") -> list:
        """Get list of words of a record. Supports both documents and groups/feeds.

        Args:
            record (Record): The record.
            sorted_by (str, optional): Sorting of words (default is weight).

        Returns:
            list: The concordance list.
        """
        kwargs = {
            'record': record,
            'sortedBy': sorted_by
        }
        return self._call_method('getConcordanceOf', args=None, kwargs={k: v for k, v in kwargs.items() if v is not None})


    def get_custom_meta_data(self, for_key: str, from_record: Record, default_value=None):
        """Get user-defined metadata from a record.

        Args:
            for_key (str): The key of the user-defined value.
            from_record (Record): The record.
            default_value (_type_, optional): Default value if user-defined metadata does not yet exist, otherwise a missing value is returned. Defaults to None.
        """
        kwargs = {
            'for': for_key,
            'from': from_record,
            'defaultValue': default_value
        }

        return self._call_method('getCustomMetaData', args=None, kwargs=kwargs)

    def get_database_with_id(self, id: int) -> Database:
        """Get database with the specified id.

        Args:
            id (int): The scripting identifier.

        Returns:
            Database: The database with the specified id.
        """
        return self._call_method('getDatabaseWithId', args=[id])

    def get_database_with_uuid(self, uuid: str) -> Database:
        """Get database with the specified uuid.

        Args:
            uuid (str): The unique identifier.

        Returns:
            Database: The database with the specified uuid.
        """
        return self._call_method('getDatabaseWithUuid', [uuid])

    def get_embedded_images_of(self, source_code: str, base_url: str = None, type: str = None) -> list:
        """Get the URLs of all embedded images of an HTML page.

        Args:
            source_code (str): The source code of the HTML page.
            base_url (str, optional): The URL of the HTML page containing the images.
            type (str, optional): The desired type of the images (e.g. JPG, GIF, PNG, ...).

        Returns:
            list: The URLs of embedded images.
        """
        kwargs = {
            'baseURL': base_url,
            'type': type
        }
        return self._call_method('getEmbeddedImagesOf', args=[source_code], kwargs={k: v for k, v in kwargs.items() if v is not None})

    def get_embedded_objects_of(self, source_code: str, base_url: str = None, type: str = None) -> list:
        """Get the URLs of all embedded objects of an HTML page.

        Args:
            source_code (str): The source code of the HTML page.
            base_url (str, optional): The URL of the HTML page containing the embedded objects.
            type (str, optional): The desired type of the objects (e.g. MOV).

        Returns:
            list: The URLs of embedded objects.
        """
        kwargs = {
            'baseURL': base_url,
            'type': type
        }
        return self._call_method('getEmbeddedObjectsOf', args=[source_code], kwargs={k: v for k, v in kwargs.items() if v is not None})

    def get_embedded_sheets_and_scripts_of(self, source_code: str, base_url: str = None, type: str = None) -> list:
        """Get the URLs of all embedded style sheets and scripts of an HTML page.

        Args:
            source_code (str): The source code of the HTML page.
            base_url (str, optional): The URL of the HTML page containing the style sheets and scripts.
            type (str, optional): The desired type of the links (e.g. CSS).

        Returns:
            list: The URLs of embedded style sheets and scripts.
        """
        kwargs = {
            'baseURL': base_url,
            'type': type
        }
        return self._call_method('getEmbeddedSheetsAndScriptsOf', args=[source_code], kwargs={k: v for k, v in kwargs.items() if v is not None})

    def get_favicon_of(self, source_code: str, base_url: str = None) -> str:
        """Get the favicon of an HTML page.

        Args:
            source_code (str): The source code of the HTML page.
            base_url (str, optional): The URL of the HTML page containing the favicon.

        Returns:
            str: The URL of the favicon.
        """
        kwargs = {
            'baseURL': base_url
        }
        return self._call_method('getFaviconOf', args=[source_code], kwargs={k: v for k, v in kwargs.items() if v is not None})

    def get_frames_of(self, source_code: str, base_url: str = None) -> list:
        """Get the URLs of all frames of an HTML page.

        Args:
            source_code (str): The source code of the HTML page.
            base_url (str, optional): The URL of the HTML page containing the frames.

        Returns:
            list: The URLs of all frames.
        """
        kwargs = {
            'baseURL': base_url
        }
        return self._call_method('getFramesOf', args=[source_code], kwargs={k: v for k, v in kwargs.items() if v is not None})

    def get_items_of_feed(self, source_code: str, base_url: str = None) -> list:
        """Get the items of a RSS, RDF or Atom feed. Dictionaries contain title, link, date, description, content, author, html (item converted to HTML), tags, and enclosures.

        Args:
            source_code (str): The source code of the feed.
            base_url (str, optional): The URL of the feed.

        Returns:
            list: The items of the feed.
        """
        kwargs = {
            'baseURL': base_url
        }
        return self._call_method('getItemsOfFeed', args=[source_code], kwargs={k: v for k, v in kwargs.items() if v is not None})

    def get_links_of(self, source_code: str, base_url: str = None, containing: str = None, type: str = None) -> list:
        """Get the URLs of all links of an HTML page.

        Args:
            source_code (str): The source code of the HTML page.
            base_url (str, optional): The URL of the HTML page containing the links.
            containing (str, optional): The case sensitive string matched against the description of links.
            type (str, optional): The desired type of the links (e.g. HTML, PHP, JPG, ...).

        Returns:
            list: The URLs of all links.
        """
        kwargs = {
            'baseURL': base_url,
            'containing': containing,
            'type': type
        }
        return self._call_method('getLinksOf', args=[source_code], kwargs={k: v for k, v in kwargs.items() if v is not None})

    def get_record_at(self, text: str, database: Optional[Database] = None) -> Record:
        """Search for record at the specified location.

        Args:
            text (str): The location of the record as a POSIX path (/ in names has to be replaced with \/, see location property).
            database (Database, optional): The database. Uses current database if not specified.

        Returns:
            Record: The record at the specified location.
        """
        return self._call_method('getRecordAt', [text], {'in': database})

    def get_record_with_id(self, identifier: int, database: Database = None) -> Record:
        """Get record with the specified id.

        Args:
            identifier (int): The scripting identifier.
            database (Database, optional): The database. Uses current database if not specified.

        Returns:
            Record: The record with the specified id.
        """
        kwargs = {
            'in': database
        }
        return self._call_method('getRecordWithId', args=[identifier], kwargs={k: v for k, v in kwargs.items() if v is not None})

    def get_record_with_uuid(self, uuid: str, database: Database = None) -> Record:
        """Get record with the specified uuid or item link.

        Args:
            uuid (str): The unique identifier or item link.
            database (Database, optional): The database. Uses all databases if not specified.

        Returns:
            Record: The record with the specified uuid or item link.
        """
        kwargs = {
            'in': database
        }
        return self._call_method('getRecordWithUuid', args=[uuid], kwargs={k: v for k, v in kwargs.items() if v is not None})

    def get_rich_text_of(self, source_code: str, base_url: str = None) -> str:
        """Get the rich text of an HTML page.

        Args:
            source_code (str): The source code of the HTML page.
            base_url (str, optional): The URL of the HTML page.

        Returns:
            str: The rich text of the HTML page.
        """
        kwargs = {
            'baseURL': base_url
        }
        return self._call_method('getRichTextOf', args=[source_code], kwargs={k: v for k, v in kwargs.items() if v is not None})

    def get_text_of(self, source_code: str) -> str:
        """Get the text of an HTML page.

        Args:
            source_code (str): The source code of the HTML page.

        Returns:
            str: The text of the HTML page.
        """
        return self._call_method('getTextOf', args=[source_code], kwargs={})

    def get_title_of(self, source_code: str) -> str:
        """Get the title of an HTML page.

        Args:
            source_code (str): The source code of the HTML page.

        Returns:
            str: The title of the HTML page.
        """
        return self._call_method('getTitleOf', args=[source_code], kwargs={})

    def hide_progress_indicator(self) -> bool:
        """Hide a visible progress indicator."""
        return self._call_method('hideProgressIndicator')
        
    def import_(self, path: str, from_: str = None, name: str = None, placeholders: Record = None, to: Record = None, type: int = None) -> Record:
        """Import a file or folder (including its subfolders).

        Args:
            path (str): The POSIX path of the file or folder.
            from_ (str, optional): The name of the source application.
            name (str, optional): The name for the imported record.
            placeholders (Record, optional): Optional placeholders as key-value-pairs for text, RTF/RTFD & HTML/XML templates and filenames. Note: The standard placeholders of .dtTemplate packages are also supported if this parameter is specified.
            to (Record, optional): The destination group. Uses incoming group or group selector if not specified.
            type (int, optional): Obsolete.

        Returns:
            Record: The imported record.
        """
        kwargs = {
            'from': from_,
            'name': name,
            'placeholders': placeholders,
            'to': to,
            'type': type
        }
        return self._call_method('import', args=[path], kwargs={k: v for k, v in kwargs.items() if v is not None})

    def import_template(self, path: str, to: Record = None) -> Record:
        """Import a template. Note: Template scripts are not supported.

        Args:
            path (str): The POSIX path of the template.
            to (Record, optional): The destination group. Uses incoming group or group selector if not specified.

        Returns:
            Record: The imported template.
        """
        kwargs = {
            'to': to
        }
        return self._call_method('importTemplate', args=[path], kwargs={k: v for k, v in kwargs.items() if v is not None})

    def indicate(self, path: str, to: Record = None, type: int = None) -> Record:
        """Indicate ('index') a file or folder (including its subfolders).

        Args:
            path (str): The POSIX path of the file or folder.
            to (Record, optional): The destination group. Uses incoming group or group selector if not specified.
            type (int, optional): Obsolete.

        Returns:
            Record: The indicated record.
        """
        kwargs = {
            'to': to,
            'type': type
        }
        return self._call_method('indicate', args=[path], kwargs={k: v for k, v in kwargs.items() if v is not None})

    def load_workspace(self, name: str) -> bool:
        """Load a workspace.

        Args:
            name (str): The name of the workspace.

        Returns:
            bool: True if successful, False otherwise.
        """
        return self._call_method('loadWorkspace', args=[name])

    def log_message(self, text: str = None, info: str = None, record: Record = None) -> bool:
        """Log info for a record, file or action to the Window > Log panel.

        Args:
            text (str, optional): The optional POSIX path or action. Not necessary for records.
            info (str, optional): Additional information. Required for records.
            record (Record, optional): The record.

        Returns:
            bool: True if successful, False otherwise.
        """
        args = [text] if text is not None else []
        kwargs = {
            'info': info,
            'record': record
        }
        return self._call_method('logMessage', args=args, kwargs={k: v for k, v in kwargs.items() if v is not None})

    def lookup_records_with_comment(self, comment: str, database: Database = None) -> list:
        """Lookup records with specified comment.

        Args:
            comment (str): The comment.
            database (Database, optional): The database. Uses current database if not specified.

        Returns:
            list: The list of records.
        """
        kwargs = {
            'in': database
        }
        return self._call_method('lookupRecordsWithComment', args=[comment], kwargs={k: v for k, v in kwargs.items() if v is not None})

    def lookup_records_with_file(self, filename: str, database: Database = None) -> list:
        """Lookup records whose last path component is the specified file.

        Args:
            filename (str): The filename.
            database (Database, optional): The database. Uses current database if not specified.

        Returns:
            list: The list of records.
        """
        kwargs = {
            'in': database
        }
        return self._call_method('lookupRecordsWithFile', args=[filename], kwargs={k: v for k, v in kwargs.items() if v is not None})

    def lookup_records_with_path(self, path: str, database: Database = None) -> list:
        """Lookup records with specified path.

        Args:
            path (str): The path.
            database (Database, optional): The database. Uses current database if not specified.

        Returns:
            list: The list of records.
        """
        kwargs = {
            'in': database
        }
        return self._call_method('lookupRecordsWithPath', args=[path], kwargs={k: v for k, v in kwargs.items() if v is not None})

    def lookup_records_with_tags(self, tags: list, any: bool = False, database: Database = None) -> list:
        """Lookup records with all or any of the specified tags.

        Args:
            tags (list): The tags.
            any (bool, optional): Lookup any or all (default) tags.
            database (Database, optional): The database. Uses current database if not specified.

        Returns:
            list: The list of records.
        """
        kwargs = {
            'any': any,
            'in': database
        }
        return self._call_method('lookupRecordsWithTags', args=[tags], kwargs={k: v for k, v in kwargs.items() if v is not None})

    def lookup_records_with_url(self, url: str, database: Database = None) -> list:
        """Lookup records with specified URL.

        Args:
            url (str): The URL (or path).
            database (Database, optional): The database. Uses current database if not specified.

        Returns:
            list: The list of records.
        """
        kwargs = {
            'in': database
        }
        return self._call_method('lookupRecordsWithURL', args=[url], kwargs={k: v for k, v in kwargs.items() if v is not None})

    def merge(self, records: List[Record], destination: Record = None) -> Record:
        """Merge either a list of records as an RTF(D)/a PDF document or merge a list of not indexed groups/tags.

        Args:
            records (list): The records to merge.
            destination (Record, optional): The destination group for the merged record. The root of the database is used if not specified.

        Returns:
            Record: The merged record.
        """
        kwargs = {
            'record': records,
            'in': destination
        }
        return self._call_method('merge', args=None, kwargs={k: v for k, v in kwargs.items() if v is not None})

    def move(self, record: Record, to: Record, from_group: Record = None) -> Record:
        """Move all instances of a record to a different group. Specify the "from" group to move a single instance to a different group.

        Args:
            record (Record): The record or a list of records to move.
            to (Record): The destination group which doesn't have to be in the same database.
            from_group (Record, optional): The source group. Only applicable if record and destination group are in the same database.

        Returns:
            Record: The record after the move.
        """
        kwargs = {
            'record': record,
            'to': to,
            'from': from_group
        }
        return self._call_method('move', args=None, kwargs={k: v for k, v in kwargs.items() if v is not None})

    def open_database(self, file_path: str) -> Database:
        """Open an existing database.

        Args:
            file_path (str): The POSIX file path of the database.

        Returns:
            Database: The opened database.
        """
        return self._call_method('open database', [file_path])

    def open_tab_for(self, think_window: ThinkWindow = None, record: Record = None, referrer: str = None, url: str = None) -> Tab:
        """Open a new tab for the specified URL or record in a think window.

        Args:
            think_window (ThinkWindow, optional): The optional think window that should open a new tab. A new window is used otherwise.
            record (Record, optional): The record to open.
            referrer (str, optional): The HTTP referrer.
            url (str, optional): The URL to open.

        Returns:
            Tab: The opened tab.
        """
        kwargs = {
            'in': think_window,
            'record': record,
            'referrer': referrer,
            'url': url
        }
        return self._call_method('openTabFor', kwargs={k: v for k, v in kwargs.items() if v is not None})

    def open_window_for(self, record: Record, force: bool = None) -> ThinkWindow:
        """Open a (new) viewer or document window for the specified record (use the 'close' command to close a window). Only recommended for viewer windows, use 'open tab for' for document windows.

        Args:
            record (Record): The record to open.
            force (bool, optional): Force DEVONthink to always open a new window, even if the record is already opened in one. Off by default.

        Returns:
            ThinkWindow: The opened window.
        """
        kwargs = {
            'record': record,
            'force': force
        }
        return self._call_method('openWindowFor', args=None, kwargs={k: v for k, v in kwargs.items() if v is not None})

    def optimize(self, database: Database) -> bool:
        """Backup & optimize a database.

        Args:
            database (Database): The database to optimize.

        Returns:
            bool: True if successful, False otherwise.
        """
        kwargs = {
            'database': database
        }
        return self._call_method('optimize', args=None, kwargs={k: v for k, v in kwargs.items() if v is not None})

    def paste_clipboard(self, to: Record = None) -> Record:
        """Create a new record with the contents of the clipboard.

        Args:
            to (Record, optional): The destination group for the new record. Uses incoming group or group selector if not specified.

        Returns:
            Record: The new record.
        """
        kwargs = {
            'to': to
        }
        return self._call_method('pasteClipboard', args=[], kwargs={k: v for k, v in kwargs.items() if v is not None})

    def perform_smart_rule(self, name: str = None, record: Record = None, trigger: str = None) -> bool:
        """Perform one or all smart rules.

        Args:
            name (str, optional): The name of the smart rule. All smart rules are used if not specified.
            record (Record, optional): The record. All records matching the smart rule(s) conditions are used if no record is specified.
            trigger (str, optional): The optional event to trigger smart rules. Can be one of "classify event", "clipping event", "consolidation event", "convert event", "creation event", "deconsolidation event", "download event", "duplicate event", "flagging event", "import event", "imprint event", "labelling event", "launch event", "move event", "no event", "OCR event", "open event", "open externally event", "rename event", "replicate event", "tagging event".

        Returns:
            bool: True if successful, False otherwise.
        """
        kwargs = {
            'name': name,
            'record': record,
            'trigger': trigger
        }
        return self._call_method('performSmartRule', args=[], kwargs={k: v for k, v in kwargs.items() if v is not None})

    def refresh(self, record: Record) -> bool:
        """Refresh a record. Currently only supported by feeds.

        Args:
            record (Record): The record to refresh.

        Returns:
            bool: True if successful, False otherwise.
        """
        return self._call_method('refresh', args=None, kwargs={'record': record})

    def replicate(self, record: Record, to: Record) -> Record:
        """Replicate a record.

        Args:
            record (Record): The record or a list of records to replicate.
            to (Record): The destination group which must be in the same database.

        Returns:
            Record: The replicated record.
        """
        return self._call_method('replicate', args=None, kwargs={'record': record, 'to': to})

    def save_workspace(self, name: str) -> bool:
        """Save a workspace.

        Args:
            name (str): The name of the workspace.

        Returns:
            bool: True if successful, False otherwise.
        """
        return self._call_method('saveWorkspace', args=[name])

    def search(self, text: str = None, comparison: str = "no case", exclude_subgroups: bool = False, in_group: Record = None) -> List[Record]:
        """Search for records in specified group or all databases.

        Args:
            text (str, optional): The search string. Supports keys, operators, and wildcards.
            comparison (str, optional): The comparison to use. Defaults to "no case". Valid values are "fuzzy", "no case", and "no umlauts".
            exclude_subgroups (bool, optional): Don't search in subgroups of the specified group. Off by default.
            in_group (Record, optional): The group to search in. Searches in all databases if not specified.

        Returns:
            list: The search results.
        """
        kwargs = {
            'comparison': comparison,
            'excludeSubgroups': exclude_subgroups,
            'in': in_group
        }
        return self._call_method('search', args=[text], kwargs={k: v for k, v in kwargs.items() if v is not None})

    def set_cell_at(self, specifier: OSAObjProxy, column: int, row: int, to: str) -> bool:
        """Set cell at specified position of current sheet.

        Args:
            specifier: The object for the command.
            column (int): Either the index (1...n) or the name of the column of the cell.
            row (int): The row (1...n) of the cell.
            to (str): The content of the cell.

        Returns:
            bool: True if successful, False otherwise.
        """
        kwargs = {
            'column': column,
            'row': row,
            'to': to
        }
        
        return self._call_method('setCellAt', args=[specifier], kwargs={k: v for k, v in kwargs.items() if v is not None})
    
    def show_progress_indicator(self, title: str, cancel_button: bool = False, steps: int = None) -> bool:
        """Show a progress indicator or update an already visible indicator. You have to ensure that the indicator is hidden again via 'hide progress indicator' when the script ends or if an error occurs.

        Args:
            title (str): The title of the progress.
            cancel_button (bool, optional): Display a button to cancel the process. Defaults to False.
            steps (int, optional): The number of steps of the progress or a negative value for an indeterminate number.

        Returns:
            bool: True if successful, False otherwise.
        """
        kwargs = {
            'cancelButton': cancel_button,
            'steps': steps
        }
        return self._call_method('showProgressIndicator', args=[title], kwargs={k: v for k, v in kwargs.items() if v is not None})

    def start_downloads(self) -> bool:
        """Start queue of download manager.

        Returns:
            bool: True if successful, False otherwise.
        """
        return self._call_method('startDownloads')

    def step_progress_indicator(self, text: str = None) -> bool:
        """Go to next step of a progress.

        Args:
            text (str, optional): The info for the current step.

        Returns:
            bool: True if successful, False otherwise.
        """
        kwargs = {
            'Text': text
        }
        return self._call_method('stepProgressIndicator', kwargs={k: v for k, v in kwargs.items() if v is not None})

    def stop_downloads(self) -> bool:
        """Stop queue of download manager.

        Returns:
            bool: True if successful, False otherwise.
        """
        return self._call_method('stopDownloads')

    def summarize_highlights_of(self, records: list, to: str, destination_group: Record = None) -> Record:
        """Summarize highlights & annotations of records. PDF, RTF(D), Markdown and web documents are currently supported.

        Args:
            records (list): The records to summarize.
            to (str): The desired format. Accepts "markdown", "rich", or "sheet".
            destination_group (Record, optional): The destination group for the summary. The current group of the database is used if not specified.

        Returns:
            Record: The summary record.
        """
        kwargs = {
            'records': records,
            'to': to,
            'in': destination_group
        }
        return self._call_method('summarizeHighlightsOf', args=None, kwargs={k: v for k, v in kwargs.items() if v is not None})

    def synchronize(self, database: Database = None, record: Record = None) -> bool:
        """Synchronizes records with the filesystem or databases with their sync locations. Only one of both operations is supported.

        Args:
            database (Database, optional): The database to synchronize via its sync locations.
            record (Record, optional): The (external) record to update. New items are added, updated ones indexed and obsolete ones removed. NOTE: This is rarely necessary as databases are usually automatically updated by filesystem events.

        Returns:
            bool: True if successful, False otherwise.
        """
        kwargs = {
            'database': database,
            'record': record
        }
        return self._call_method('synchronize', args=None, kwargs={k: v for k, v in kwargs.items() if v is not None})

    def update_thumbnail(self, record: Record) -> bool:
        """Update existing thumbnail of a record. Thumbnailing is performed asynchronously in the background.
        
        Args:
            record (Record): The record.
        
        Returns:
            bool: True if successful, False otherwise.
        """
        kwargs = {
            'of': record
        }
        return self._call_method('updateThumbnail', args=None, kwargs={k: v for k, v in kwargs.items() if v is not None})

    def verify(self, database: Database) -> int:
        """Verify a database. Returns total number of errors, invalid filenames, and missing files.

        Args:
            database (Database): The database to verify.

        Returns:
            int: The total number of errors, invalid filenames, and missing files.
        """
        return self._call_method('verify', args=[database])

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