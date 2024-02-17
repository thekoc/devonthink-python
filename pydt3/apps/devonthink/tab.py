from typing import List, TYPE_CHECKING

from ...helper_bridging import OSAObjProxy

if TYPE_CHECKING:
    from ..devonthink import Record, Database, Text, ThinkWindow

class Tab(OSAObjProxy):
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
        return self._call_method('currentMovieFrame')

    @property
    def current_page(self) -> int:
        """Zero-based index of current PDF page."""
        return self._call_method('currentPage')

    @current_page.setter
    def current_page(self, value: int):
        self._set_property('currentPage', value)

    @property
    def current_time(self) -> float:
        """Time of current movie frame."""
        return self._call_method('currentTime')

    @current_time.setter
    def current_time(self, value: float):
        self._set_property('currentTime', value)

    @property
    def database(self) -> 'Database':
        """The database of the tab."""
        return self._get_property('database')

    @property
    def id(self) -> int:
        """The unique identifier of the tab."""
        return self._call_method('id')

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
    def paginated_pdf(self):
        """A printed PDF with pagination of the visible document."""
        return self._call_method('paginatedPDF')

    @property
    def pdf(self):
        """A PDF without pagination of the visible document retaining the screen layout."""
        return self._call_method('pdf')

    @property
    def reference_url(self) -> str:
        """The URL to reference/link back to the current content record and its selection, page, frame etc."""
        return self._call_method('referenceURL')

    @property
    def selected_column(self) -> int:
        """Index of selected column of the current sheet."""
        return self._call_method('selectedColumn')

    @selected_column.setter
    def selected_column(self, value: int):
        self._set_property('selectedColumn', value)

    @property
    def selected_columns(self) -> List[int]:
        """Indices of selected columns of the current sheet."""
        return self._call_method('selectedColumns')

    @property
    def selected_row(self) -> int:
        """Index of selected row of the current sheet."""
        return self._call_method('selectedRow')

    @selected_row.setter
    def selected_row(self, value: int):
        self._set_property('selectedRow', value)

    @property
    def selected_rows(self) -> List[int]:
        """Indices of selected rows of the current sheet."""
        return self._call_method('selectedRows')

    @property
    def selected_text(self) -> 'Text':
        """The text container for the selection of the tab."""
        return self._call_method('selectedText')

    @property
    def source(self) -> str:
        """The HTML source of the current web page."""
        return self._call_method('source')

    @property
    def text(self) -> 'Text':
        """The text container of the tab."""
        return self._get_property('text')

    @text.setter
    def text(self, value: str):
        self._set_property('text', value)

    @property
    def think_window(self) -> 'ThinkWindow':
        """The think window of the tab."""
        return self._get_property('thinkWindow')

    @property
    def url(self) -> str:
        """The URL of the current web page. Setting the URL can be used to load a web page."""
        return self._call_method('url')

    @url.setter
    def url(self, value: str):
        self._set_property('url', value)

    @property
    def web_archive(self):
        """Web archive of the current web page."""
        return self._call_method('webArchive')
