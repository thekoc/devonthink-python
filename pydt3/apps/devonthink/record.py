
import datetime

from typing import Optional, List, Any, TYPE_CHECKING

from .devonthink import DEVONthink3
from ...osascript import OSAScript
from ...helper_bridging import OSAObjProxy, OSAObjArray


if TYPE_CHECKING:
    from .database import Database
    from .reminder import Reminder
    from .text import Text

class CustomMetaData:
    def __init__(self, owner: 'Record', property_name: str):
        self.owner = owner
        self.meta_dict = owner._get_property(property_name)
        self.property_name = property_name
        self._helper_script = owner._helper_script
        self._app = DEVONthink3.from_script(self._helper_script)

    def get_dict_value(self):
        value = self.meta_dict();
        if value is None:
            value = {}
        return value

    def items(self):
        return self.get_dict_value().items()
    
    def asdict(self):
        return self.get_dict_value()
    
    def __getitem__(self, key: str) -> Any:
        return self._app.get_custom_meta_data(key, self.owner)

    def __setitem__(self, key: str, value: Any):
        return self._app.add_custom_meta_data(value, key, self.owner)

    def __repr__(self) -> str:
        return f'<{type(self).__name__}: {self.get_dict_value()}>'

class Record(OSAObjProxy):
    # elements
    @property
    def children(self) -> OSAObjArray['Record']:
        """List of child records."""
        return self._get_property('children')

    @property
    def incoming_references(self) -> OSAObjArray['Record']:
        """List of records referencing this record."""
        return self._get_property('incomingReferences')

    @property
    def incoming_wiki_references(self) -> OSAObjArray['Record']:
        """List of wiki records referencing this record."""
        return self._get_property('incomingWikiReferences')

    @property
    def outgoing_references(self) -> OSAObjArray['Record']:
        """List of records this record references."""
        return self._get_property('outgoingReferences')

    @property
    def outgoing_wiki_references(self) -> OSAObjArray['Record']:
        """List of wiki records this record references."""
        return self._get_property('outgoingWikiReferences')

    @property
    def parents(self) -> OSAObjArray['Record']:
        """List of parent records."""
        return self._get_property('parents')

    @property
    def texts(self):
        """List of texts of the record. (Not implemented. It is broken in JXA.)"""
        raise NotImplementedError('Not implemented. It is broken in JXA.')  

    # properties
    @property
    def addition_date(self) -> datetime.datetime:
        """Date when the record was added to the database."""
        return self._call_method('additionDate')

    @property
    def aliases(self) -> str:
        """Wiki aliases (separated by commas or semicolons) of a record."""
        return self._call_method('aliases')

    @aliases.setter
    def aliases(self, value: str):
        self._set_property('aliases', value)

    @property
    def all_document_dates(self) -> Optional[List[datetime.datetime]]:
        """All dates extracted from text of document, e.g. a scan."""
        return self._call_method('allDocumentDates')

    @property
    def altitude(self) -> float:
        """The altitude in metres of a record."""
        return self._call_method('altitude')

    @altitude.setter
    def altitude(self, value: float):
        self._set_property('altitude', value)

    @property
    def annotation(self) -> Optional['Record']:
        """Annotation of a record. Only plain & rich text and Markdown documents are supported."""
        return self._call_method('annotation')

    @annotation.setter
    def annotation(self, value: 'Record'):
        self._set_property('annotation', value)

    @property
    def annotation_count(self) -> int:
        """The number of annotations. Currently only supported for PDF documents."""
        return self._call_method('annotationCount')

    @property
    def attached_script(self) -> str:
        """POSIX path of script attached to a record."""
        return self._call_method('attachedScript')

    @attached_script.setter
    def attached_script(self, value: str):
        self._set_property('attachedScript', value)

    @property
    def attachment_count(self) -> int:
        """The number of attachments. Currently only supported for RTFD documents and emails."""
        return self._call_method('attachmentCount')

    @property
    def bates_number(self) -> int:
        """Bates number."""
        return self._call_method('batesNumber')

    @bates_number.setter
    def bates_number(self, value: int):
        self._set_property('batesNumber', value)
        
    @property
    def cells(self) -> Optional[OSAObjArray[OSAObjArray[str]]]:
        """The cells of a sheet. This is a list of rows, each row contains a list of string values for the various colums."""
        raise NotImplementedError('Not implemented. It is broken in JXA.')
        # return self._get_property('cells')

    @property
    def character_count(self) -> int:
        """The character count of a record."""
        return self._call_method('characterCount')

    @property
    def color(self) -> Optional[List[float]]:
        """The color of a record. Currently only supported by tags."""
        return self._call_method('color')

    @color.setter
    def color(self, value: OSAObjArray[float]):
        self._set_property('color', value)

    @property
    def columns(self) -> Optional[List[str]]:
        """The column names of a sheet.""" 
        return self._call_method('columns')

    @property
    def comment(self) -> str:
        """The comment of a record."""
        return self._call_method('comment')

    @comment.setter
    def comment(self, value: str):
        self._set_property('comment', value)

    @property
    def content_hash(self) -> Optional[str]:
        """Stored SHA1 hash of files and document packages."""
        return self._call_method('contentHash')

    @property
    def creation_date(self) -> datetime.datetime:
        """The creation date of a record."""
        return self._call_method('creationDate')

    @property
    def custom_meta_data(self) -> Optional[CustomMetaData]:
        """User-defined metadata of a record as a dictionary containing key-value pairs. Setting a value for an unknown key automatically adds a definition to Preferences > Data."""
        return CustomMetaData(self, 'customMetaData')

    @property
    def data(self) -> str:
        """The file data of a record. Currently only supported by PDF documents, images, rich texts and web archives."""
        return self._call_method('data')

    @property
    def database(self) -> 'Database':
        """The database of the record."""
        return self._get_property('database')

    @property
    def date(self) -> datetime.datetime:
        """The (creation/modification) date of a record."""
        return self._call_method('date')

    @property
    def digital_object_identifier(self) -> Optional[str]:
        """Digital object identifier (DOI) extracted from text of document, e.g. a scanned receipt."""
        return self._call_method('digitalObjectIdentifier')

    @property
    def dimensions(self) -> List[int]:
        """The width and height of an image or PDF document in pixels."""
        return self._call_method('dimensions')

    @property
    def document_amount(self) -> Optional[str]:
        """Amount extracted from text of document, e.g. a scanned receipt."""
        return self._call_method('documentAmount')

    @property
    def document_date(self) -> Optional[datetime.datetime]:
        """First date extracted from text of document, e.g. a scan."""
        return self._call_method('documentDate')

    @property
    def document_name(self) -> str:
        """Name based on text or properties of document"""
        return self._call_method('documentName')

    @property
    def dpi(self) -> int:
        """The resultion of an image in dpi."""
        return self._call_method('dpi')

    @property
    def duplicates(self) -> OSAObjArray['Record']:
        """The duplicates of a record (only other instances, not including the record)."""
        result = self._get_property('duplicates')
        return result

    @property
    def duration(self) -> float:
        """The duration of audio and video files."""
        return self._call_method('duration')

    @property
    def encrypted(self) -> bool:
        """Specifies if a document is encrypted or not. Currently only supported by PDF documents."""
        return self._call_method('encrypted')

    @property
    def exclude_from_classification(self) -> bool:
        """Exclude group or record from classifying."""
        return self._call_method('excludeFromClassification')

    @exclude_from_classification.setter
    def exclude_from_classification(self, value: bool):
        self._set_property('excludeFromClassification', value)

    @property
    def exclude_from_search(self) -> bool:
        """Exclude group or record from searching."""
        return self._call_method('excludeFromSearch')

    @exclude_from_search.setter
    def exclude_from_search(self, value: bool):
        self._set_property('excludeFromSearch', value)

    @property
    def exclude_from_see_also(self) -> bool:
        """Exclude record from see also."""
        return self._call_method('excludeFromSeeAlso')

    @exclude_from_see_also.setter
    def exclude_from_see_also(self, value: bool):
        self._set_property('excludeFromSeeAlso', value)

    @property
    def exclude_from_tagging(self) -> bool:
        """Exclude group from tagging."""
        return self._call_method('excludeFromTagging')

    @exclude_from_tagging.setter
    def exclude_from_tagging(self, value: bool):
        self._set_property('excludeFromTagging', value)

    @property
    def exclude_from_wiki_linking(self) -> bool:
        """Exclude record from automatic Wiki linking."""
        return self._call_method('excludeFromWikiLinking')

    @exclude_from_wiki_linking.setter
    def exclude_from_wiki_linking(self, value: bool):
        self._set_property('excludeFromWikiLinking', value)

    @property
    def filename(self) -> str:
        """The current filename of a record."""
        return self._call_method('filename')

    @property
    def geolocation(self) -> Optional[str]:
        """The human readable geogr. place of a record."""
        return self._call_method('geolocation')

    @property
    def height(self) -> int:
        """The height of an image or PDF document in pixels."""
        return self._call_method('height')

    @property
    def id(self) -> int:
        """The scripting identifier of a record. Optimizing or closing a database might modify this identifier."""
        return self._call_method('id')

    @property
    def image(self) -> Any:
        """The image or PDF document of a record. Setting supports both raw data and strings containing paths or URLs."""
        return self._call_method('image')

    @image.setter
    def image(self, value):
        self._set_property('image', value)

    @property
    def indexed(self) -> bool:
        """Indexed or imported record."""
        return self._call_method('indexed')

    @property
    def interval(self) -> float:
        """Refresh interval of a feed. Currently overriden by preferences."""
        return self._call_method('interval')

    @interval.setter
    def interval(self, value: float):
        self._set_property('interval', value)

    @property
    def kind(self) -> Optional[str]:
        """The human readable and localized kind of a record. WARNING: Don't use this to check the type of a record, otherwise your script might fail depending on the version and the localization."""
        return self._call_method('kind')

    @property
    def label(self) -> int:
        """Index of label (0-7) of a record."""
        return self._call_method('label')

    @label.setter
    def label(self, value: int):
        self._set_property('label', value)

    @property
    def latitude(self) -> float:
        """The latitude in degrees of a record."""
        return self._call_method('latitude')

    @latitude.setter
    def latitude(self, value: float):
        self._set_property('latitude', value)

    @property
    def location(self) -> str:
        """The primary location in the database as a POSIX path (/ in names is replaced with \/). 
        This is the location of the first parent group."""
        return self._call_method('location')

    @property
    def location_group(self) -> 'Record':
        """The group of the record's primary location. This is identical to the first parent group."""
        return self._get_property('locationGroup')

    @property
    def locking(self) -> bool:
        """The locking of a record."""
        return self._call_method('locking')

    @locking.setter
    def locking(self, value: bool):
        self._set_property('locking', value)

    @property
    def longitude(self) -> float:
        """The longitude in degrees of a record."""
        return self._call_method('longitude')

    @longitude.setter
    def longitude(self, value: float):
        self._set_property('longitude', value)

    @property
    def meta_data(self) -> Optional[dict]:
        """Document metadata (e.g. of PDF or RTF) of a record as a dictionary containing key-value pairs. 
        Possible keys are currently kMDItemTitle, kMDItemHeadline, kMDItemSubject, kMDItemDescription, 
        kMDItemCopyright, kMDItemComment, kMDItemURL, kMDItemKeywords, kM"""
        return self._call_method('metaData')

    @property
    def mime_type(self) -> Optional[str]:
        """The (proposed) MIME type of a record."""
        return self._call_method('mimeType')

    @property
    def modification_date(self) -> datetime.datetime:
        """The modification date of a record."""
        return self._call_method('modificationDate')

    @modification_date.setter
    def modification_date(self, value: datetime.datetime):
        # TODO: Implement change of modification date
        return self._set_property('modificationDate', value)

    @property
    def name(self) -> str:
        """The name of a record."""
        return self._call_method('name')

    @name.setter
    def name(self, value: str):
        self._set_property('name', value)

    @property
    def name_without_date(self) -> str:
        """The name of a record without any dates."""
        return self._call_method('nameWithoutDate')

    @property
    def name_without_extension(self) -> str:
        """The name of a record without a file extension (independent of preferences)."""
        return self._call_method('nameWithoutExtension')

    @property
    def newest_document_date(self) -> Optional[datetime.datetime]:
        """Newest date extracted from text of document, e.g. a scan."""
        return self._call_method('newestDocumentDate')

    @property
    def number_of_duplicates(self) -> int:
        """The number of duplicates of a record."""
        return self._call_method('numberOfDuplicates')

    @property
    def number_of_hits(self) -> int:
        """The number of hits of a record."""
        return self._call_method('numberOfHits')

    @number_of_hits.setter
    def number_of_hits(self, value: int):
        self._set_property('numberOfHits', value)

    @property
    def number_of_replicants(self) -> int:
        """The number of replicants of a record."""
        return self._call_method('numberOfReplicants')

    @property
    def oldest_document_date(self) -> Optional[datetime.datetime]:
        """Oldest date extracted from text of document, e.g. a scan."""
        return self._call_method('oldestDocumentDate')

    @property
    def opening_date(self) -> Optional[datetime.datetime]:
        """Date when a content was opened the last time or when a feed was refreshed the last time."""
        return self._call_method('openingDate')

    @property
    def page_count(self) -> int:
        """The page count of a record. Currently only supported by PDF documents."""
        return self._call_method('pageCount')

    @property
    def paginated_pdf(self):
        """A printed/converted PDF of the record."""
        return self._call_method('paginatedPDF')

    @property
    def path(self) -> str:
        """The POSIX file path of a record. Only the path of external records can be changed."""
        return self._call_method('path')
    
    @path.setter
    def path(self, value: str):
        self._set_property('path', value)

    @property
    def pending(self) -> bool:
        """Flag whether the (latest) contents of a record haven't been downloaded from a sync location yet."""
        return self._call_method('pending')

    @property
    def plain_text(self) -> str:
        """The plain text of a record."""
        return self._call_method('plainText')
    
    @plain_text.setter
    def plain_text(self, value: str):
        self._set_property('plainText', value)

    @property
    def proposed_filename(self) -> str:
        """The proposed filename for a record."""
        return self._call_method('proposedFilename')

    @property
    def rating(self) -> int:
        """Rating (0-5) of a record."""
        return self._call_method('rating')

    @rating.setter
    def rating(self, value: int):
        self._set_property('rating', value)

    @property
    def reference_url(self) -> str:
        """The URL (x-devonthink-item://...) to reference/link back to a record.
        Append ?page= to specify the zero-based index of a page of a PDF document,
        ?time= to specify the time of a movie or ?search= to specify a string to search.
        """
        return self._call_method('referenceURL')

    @property
    def reminder(self) -> Optional['Reminder']:
        """Reminder of a record."""
        return self._call_method('reminder')

    @reminder.setter
    def reminder(self, value: 'Reminder'):
        self._set_property('reminder', value)

    @property
    def rich_text(self) -> 'Text':
        """The rich text of a record (see text suite). 
        Use the 'text' relationship introduced by version 3.0 instead,
        especially for changing the contents/styles of RTF(D) documents."""

        text = self._get_property('richText')
        if text.class_name == 'unknown':
            return None

    @property
    def score(self) -> float:
        """The score of the last comparison, classification or search (value between 0.0 and 1.0) or undefined otherwise."""
        return self._call_method('score')

    @property
    def size(self) -> int:
        """The size of a record in bytes."""
        return self._call_method('size')

    @property
    def source(self) -> str:
        """The HTML/XML source of a record if available or the record converted to HTML if possible."""
        return self._call_method('source')

    @property
    def state(self) -> bool:
        """The state/flag of a record."""
        return self._call_method('state')

    @state.setter
    def state(self, value: bool):
        self._set_property('state', value)

    @property
    def state_visibility(self) -> bool:
        """Obsolete."""
        raise NotImplementedError()

    @property
    def tag_type(self) -> str:
        """The tag type of a record."""
        return self._call_method('tagType')

    @property
    def tags(self) -> OSAObjArray[str]:
        """The tags of a record."""
        return self._call_method('tags')

    @tags.setter
    def tags(self, value: list):
        self._set_property('tags', value)

    @property
    def thumbnail(self) -> Optional[str]:
        """The thumbnail of a record. Setting supports both raw data and strings containing paths or URLs."""
        return self._call_method('thumbnail')

    @thumbnail.setter
    def thumbnail(self, value: any):
        self._set_property('thumbnail', value)

    @property
    def type(self) -> str:
        """
        The type of a record. ("bookmark"/‌"feed"/‌"formatted note"/‌"group"/‌"html"/‌"markdown"/‌"PDF document"/‌"picture"/‌"plist"/‌"quicktime"/‌"rtf"/‌"rtfd"/‌"script"/‌"sheet"/‌"smart group"/‌"txt"/‌"unknown"/‌"webarchive"/‌"xml")
        Note: In compiled menu/toolbar scripts you might have to use a string representation of the type for comparisons.
        """
        return self._call_method('type')

    @property
    def unread(self) -> bool:
        """The unread flag of a record."""
        return self._call_method('unread')

    @unread.setter
    def unread(self, value: bool):
        self._set_property('unread', value)

    @property
    def url(self) -> str:
        """The URL of a record."""
        return self._call_method('url')

    @property
    def uuid(self) -> str:
        """The unique and persistent identifier of a record."""
        return self._call_method('uuid')

    @property
    def web_archive(self):
        """The web archive of a record if available or the record converted to web archive if possible."""
        return self._call_method('webArchive')

    @property
    def width(self) -> int:
        """The width of an image or PDF document in pixels."""
        return self._call_method('width')

    @property
    def word_count(self) -> int:
        """The word count of a record."""
        return self._call_method('wordCount')
    
    def __repr__(self):
        return f'<Record: {self.name}>'
