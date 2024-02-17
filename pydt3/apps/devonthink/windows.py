
from typing import List, TYPE_CHECKING

from ...helper_bridging import OSAObjProxy

if TYPE_CHECKING:
    from ..devonthink import Record, Database, Text, Tab


class ThinkWindow(OSAObjProxy):
    # elements
    @property
    def tabs(self) -> List['Tab']:
        """Whether the window contains tabs"""
        return self._call_method('containsTabs')

    # properties
    @property
    def content_record(self) -> 'Record':
        """The record of the visible document."""
        return self._get_property('contentRecord')

    @property
    def current_line(self) -> int:
        """Zero-based index of current line."""
        return self._call_method('currentLine')

    @property
    def current_movie_frame(self):
        """Thumbnail of current movie frame."""
        raise NotImplementedError()

    @property
    def current_page(self) -> int:
        """Zero-based index of current PDF page."""
        return self._call_method('currentPage')

    @current_page.setter
    def current_page(self, value: int):
        self._set_property('currentPage', value)

    @property
    def current_tab(self) -> 'Tab':
        """The selected tab of the think window."""
        return self._get_property('currentTab')

    @property
    def current_time(self) -> float:
        """Time of current movie frame."""
        return self._call_method('currentTime')

    @property
    def database(self) -> 'Database':
        """The database of the window."""
        return self._get_property('database')

    @property
    def loading(self) -> bool:
        """Specifies if the current web page is still loading."""
        return self._call_method('loading')

    @property
    def number_of_columns(self) -> int:
        """Number of columns of the current sheet."""
        return self._call_method('numberOfColumns')

    @property
    def number_of_rows(self) -> int:
        """Number of rows of the current sheet."""
        return self._call_method('numberOfRows')

    @property
    def paginated_pdf(self) -> str:
        """A printed PDF with pagination of the visible document."""
        return self._call_method('paginatedPDF')

    @property
    def pdf(self) -> str:
        """A PDF without pagination of the visible document retaining the screen layout."""
        return self._call_method('pdf')

    @property
    def selected_column(self) -> int:
        """Index (1...n) of selected column of the current sheet."""
        return self._call_method('selectedColumn')

    @selected_column.setter
    def selected_column(self, value: int):
        self._set_property('selectedColumn', value)

    @property
    def selected_columns(self) -> List[int]:
        """Indices (1...n) of selected columns of the current sheet."""
        return self._call_method('selectedColumns')

    @property
    def selected_row(self) -> int:
        """Index (1...n) of selected row of the current sheet."""
        return self._call_method('selectedRow')

    @selected_row.setter
    def selected_row(self, value: int):
        self._set_property('selectedRow', value)

    @property
    def selected_rows(self) -> List[int]:
        """Indices (1...n) of selected rows of the current sheet."""
        return self._call_method('selectedRows')

    @property
    def selected_text(self) -> 'Text':
        """The text container for the selection of the window."""
        return self._get_property('selectedText')
    
    @selected_text.setter
    def selected_text(self, value: str):
        self._set_property('selectedText', value)
    
    @property
    def source(self) -> str:
        """The HTML source of the current web page."""
        return self._call_method('source')

    @property
    def text(self) -> 'Text':
        """The text container of the window."""
        return self._get_property('text')

    @text.setter
    def text(self, value: str):
        self._set_property('text', value)

    @property
    def url(self) -> str:
        """The URL of the current web page. In addition, setting the URL can be used to load a web page."""
        return self._call_method('url')

    @url.setter
    def url(self, value: str):
        self._set_property('url', value)

    @property
    def web_archive(self) -> str:
        """Web archive of the current web page."""
        return self._call_method('webArchive')

class DocumentWindow(ThinkWindow):
    @property
    def record(self) -> 'Record':
        """The record of the visible document."""
        return self._get_property('record')

class ViewerWindow(ThinkWindow):
    # elements
    @property
    def selected_records(self) -> List['Record']:
        """List of selected records in the viewer."""
        return self.get_element_array('selectedRecords')

    # properties
    @property
    def root(self) -> 'Record':
        """The top level group of the viewer."""
        return self._get_property('root')

    @root.setter
    def root(self, value: 'Record'):
        self._set_property('root', value)

    @property
    def search_query(self) -> str:
        """The search query. Setting the query performs a search."""
        return self._call_method('searchQuery')

    @search_query.setter
    def search_query(self, value: str):
        self._set_property('searchQuery', value)

    @property
    def search_results(self) -> list:
        """The search results."""
        return self._get_property('searchResults')

    @property
    def selection(self) -> list:
        """The current selection."""
        raise NotImplementedError()


