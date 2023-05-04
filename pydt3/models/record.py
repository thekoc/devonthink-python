
from typing import List, Optional
from ..osascript import OSAScript, OSAObjProxy

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .database import Database
    from .reminder import Reminder

class Record(OSAObjProxy):
    def __init__(self, script: 'OSAScript', obj_id: int, class_name: str):
        super().__init__(script, obj_id, class_name)

    # elements
    @property
    def children(self) -> List['Record']:
        """List of child records."""
        return self.get_property_native('children')

    @property
    def incoming_references(self) -> List['Record']:
        """List of records referencing this record."""
        return self.get_property_native('incomingReferences')

    @property
    def incoming_wiki_references(self) -> List['Record']:
        """List of wiki records referencing this record."""
        return [proxy.as_class(Record) for proxy in self.get_property_native('incomingWikiReferences')]

    @property
    def outgoing_references(self) -> List['Record']:
        """List of records this record references."""
        return [proxy.as_class(Record) for proxy in self.get_property_native('outgoingReferences')]

    @property
    def outgoing_wiki_references(self) -> List['Record']:
        """List of wiki records this record references."""
        return [proxy.as_class(Record) for proxy in self.get_property_native('outgoingWikiReferences')]

    @property
    def parents(self) -> List['Record']:
        """List of parent records."""
        return self.get_property_native('parents')

    @property
    def texts(self):
        """List of texts of the record."""
        raise NotImplementedError()  

    # properties
    @property
    def addition_date(self) -> str:
        """Date when the record was added to the database."""
        return self.get_property_native('additionDate')

    @property
    def aliases(self) -> str:
        """Wiki aliases (separated by commas or semicolons) of a record."""
        return self.get_property_native('aliases')

    @aliases.setter
    def aliases(self, value: str):
        self.set_property('aliases', value)

    @property
    def all_document_dates(self) -> Optional[List[str]]:
        """All dates extracted from text of document, e.g. a scan."""
        return self.get_property_native('allDocumentDates')

    @property
    def altitude(self) -> float:
        """The altitude in metres of a record."""
        return self.get_property_native('altitude')

    @altitude.setter
    def altitude(self, value: float):
        self.set_property('altitude', value)

    @property
    def annotation(self) -> Optional['Record']:
        """Annotation of a record. Only plain & rich text and Markdown documents are supported."""
        return self.get_property_native('annotation')

    @annotation.setter
    def annotation(self, value: 'Record'):
        self.set_property('annotation', value)

    @property
    def annotation_count(self) -> int:
        """The number of annotations. Currently only supported for PDF documents."""
        return self.get_property_native('annotationCount')

    @property
    def attached_script(self) -> str:
        """POSIX path of script attached to a record."""
        return self.get_property_native('attachedScript')

    @attached_script.setter
    def attached_script(self, value: str):
        self.set_property('attachedScript', value)

    @property
    def attachment_count(self) -> int:
        """The number of attachments. Currently only supported for RTFD documents and emails."""
        return self.get_property_native('attachmentCount')

    @property
    def bates_number(self) -> int:
        """Bates number."""
        return self.get_property_native('batesNumber')

    @bates_number.setter
    def bates_number(self, value: int):
        self.set_property('batesNumber', value)
        
    @property
    def cells(self) -> Optional[List[List[str]]]:
        """The cells of a sheet. This is a list of rows, each row contains a list of string values for the various colums."""
        return self.get_property_native('cells')

    @property
    def character_count(self) -> int:
        """The character count of a record."""
        return self.get_property_native('characterCount')

    @property
    def color(self) -> Optional[List[float]]:
        """The color of a record. Currently only supported by tags."""
        return self.get_property_native('color')

    @color.setter
    def color(self, value: List[float]):
        "There seems to be a bug when setting the color "
        raise NotImplementedError()

    @property
    def columns(self) -> Optional[List[str]]:
        """The column names of a sheet.""" 
        return self.get_property_native('columns')

    @property
    def comment(self) -> str:
        """The comment of a record."""
        return self.get_property_native('comment')

    @comment.setter
    def comment(self, value: str):
        self.set_property('comment', value)

    @property
    def content_hash(self) -> Optional[str]:
        """Stored SHA1 hash of files and document packages."""
        return self.get_property_native('contentHash')

    @property
    def creation_date(self) -> str:
        """The creation date of a record."""
        return self.get_property_native('creationDate')

    @property
    def custom_meta_data(self) -> Optional[dict]:
        """User-defined metadata of a record as a dictionary containing key-value pairs. Setting a value for an unknown key automatically adds a definition to Preferences > Data."""
        return self.get_property_native('customMetaData')

    @property
    def data(self) -> str:
        """The file data of a record. Currently only supported by PDF documents, images, rich texts and web archives."""
        return self.get_property_native('data')

    @property
    def database(self) -> 'Database':
        """The database of the record."""
        return self.get_property_native('database')

    @property
    def date(self) -> str:
        """The (creation/modification) date of a record."""
        return self.get_property_native('date')

    @property
    def digital_object_identifier(self) -> Optional[str]:
        """Digital object identifier (DOI) extracted from text of document, e.g. a scanned receipt."""
        return self.get_property_native('digitalObjectIdentifier')

    @property
    def dimensions(self) -> List[int]:
        """The width and height of an image or PDF document in pixels."""
        return self.get_property_native('dimensions')

    @property
    def document_amount(self) -> Optional[str]:
        """Amount extracted from text of document, e.g. a scanned receipt."""
        return self.get_property_native('documentAmount')

    @property
    def document_date(self) -> Optional[str]:
        """First date extracted from text of document, e.g. a scan."""
        return self.get_property_native('documentDate')

    @property
    def document_name(self) -> str:
        """Name based on text or properties of document"""
        return self.get_property_native('documentName')

    @property
    def dpi(self) -> int:
        """The resultion of an image in dpi."""
        return self.get_property_native('dpi')

    @property
    def duplicates(self) -> List['Record']:
        """The duplicates of a record (only other instances, not including the record)."""
        # WARN: In applescript the class is not rightly defined, so this is a workaround
        result = self.get_property_native('duplicates')
        return [i.as_class(Record) for i in result]

    @property
    def duration(self) -> float:
        """The duration of audio and video files."""
        return self.get_property_native('duration')

    @property
    def encrypted(self) -> bool:
        """Specifies if a document is encrypted or not. Currently only supported by PDF documents."""
        return self.get_property_native('encrypted')

    @property
    def filename(self) -> str:
        """The current filename of a record."""
        return self.get_property_native('filename')

    @property
    def exclude_from_classification(self) -> bool:
        """Exclude group or record from classifying."""
        return self.get_property_native('excludeFromClassification')

    @exclude_from_classification.setter
    def exclude_from_classification(self, value: bool):
        self.set_property('excludeFromClassification', value)

    @property
    def exclude_from_search(self) -> bool:
        """Exclude group or record from searching."""
        return self.get_property_native('excludeFromSearch')

    @exclude_from_search.setter
    def exclude_from_search(self, value: bool):
        self.set_property('excludeFromSearch', value)

    @property
    def exclude_from_see_also(self) -> bool:
        """Exclude record from see also."""
        return self.get_property_native('excludeFromSeeAlso')

    @exclude_from_see_also.setter
    def exclude_from_see_also(self, value: bool):
        self.set_property('excludeFromSeeAlso', value)

    @property
    def exclude_from_tagging(self) -> bool:
        """Exclude group from tagging."""
        return self.get_property_native('excludeFromTagging')

    @exclude_from_tagging.setter
    def exclude_from_tagging(self, value: bool):
        self.set_property('excludeFromTagging', value)

    @property
    def exclude_from_wiki_linking(self) -> bool:
        """Exclude record from automatic Wiki linking."""
        return self.get_property_native('excludeFromWikiLinking')

    @exclude_from_wiki_linking.setter
    def exclude_from_wiki_linking(self, value: bool):
        self.set_property('excludeFromWikiLinking', value)

    @property
    def filename(self) -> str:
        """The current filename of a record."""
        return self.get_property_native('filename')

    @property
    def geolocation(self) -> Optional[str]:
        """The human readable geogr. place of a record."""
        return self.get_property_native('geolocation')

    @property
    def height(self) -> int:
        """The height of an image or PDF document in pixels."""
        return self.get_property_native('height')

    @property
    def id(self) -> int:
        """The scripting identifier of a record. Optimizing or closing a database might modify this identifier."""
        return self.get_property_native('id')

    # properties
    @property
    def image(self):
        """The image or PDF document of a record. Setting supports both raw data and strings containing paths or URLs."""
        return self.get_property_native('image')

    @image.setter
    def image(self, value):
        self.set_property('image', value)

    @property
    def indexed(self) -> bool:
        """Indexed or imported record."""
        return self.get_property_native('indexed')

    @property
    def interval(self) -> float:
        """Refresh interval of a feed. Currently overriden by preferences."""
        return self.get_property_native('interval')

    @interval.setter
    def interval(self, value: float):
        self.set_property('interval', value)

    @property
    def kind(self) -> Optional[str]:
        """The human readable and localized kind of a record. WARNING: Don't use this to check the type of a record, otherwise your script might fail depending on the version and the localization."""
        return self.get_property_native('kind')

    @property
    def label(self) -> int:
        """Index of label (0-7) of a record."""
        return self.get_property_native('label')

    @label.setter
    def label(self, value: int):
        self.set_property('label', value)
    @property
    def latitude(self) -> float:
        """The latitude in degrees of a record."""
        return self.get_property_native('latitude')

    @latitude.setter
    def latitude(self, value: float):
        self.set_property('latitude', value)

    @property
    def location(self) -> str:
        """The primary location in the database as a POSIX path (/ in names is replaced with \/). 
        This is the location of the first parent group."""
        return self.get_property_native('location')

    @property
    def location_group(self) -> 'Record':
        """The group of the record's primary location. This is identical to the first parent group."""
        return self.get_property_native('locationGroup')

    @property
    def locking(self) -> bool:
        """The locking of a record."""
        return self.get_property_native('locking')

    @locking.setter
    def locking(self, value: bool):
        self.set_property('locking', value)

    @property
    def longitude(self) -> float:
        """The longitude in degrees of a record."""
        return self.get_property_native('longitude')

    @longitude.setter
    def longitude(self, value: float):
        self.set_property('longitude', value)

    @property
    def meta_data(self) -> Optional[dict]:
        """Document metadata (e.g. of PDF or RTF) of a record as a dictionary containing key-value pairs. 
        Possible keys are currently kMDItemTitle, kMDItemHeadline, kMDItemSubject, kMDItemDescription, 
        kMDItemCopyright, kMDItemComment, kMDItemURL, kMDItemKeywords, kM"""
        return self.get_property_native('metaData')

    @property
    def mime_type(self) -> Optional[str]:
        """The (proposed) MIME type of a record."""
        return self.get_property_native('mimeType')

    @property
    def modification_date(self) -> str:
        """The modification date of a record."""
        return self.get_property_native('modificationDate')

    @modification_date.setter
    def modification_date(self, value: str):
        raise NotImplementedError()

    @property
    def name(self) -> str:
        """The name of a record."""
        return self.get_property_native('name')

    @name.setter
    def name(self, value: str):
        self.set_property('name', value)

    @property
    def name_without_date(self) -> str:
        """The name of a record without any dates."""
        return self.get_property_native('nameWithoutDate')

    @property
    def name_without_extension(self) -> str:
        """The name of a record without a file extension (independent of preferences)."""
        return self.get_property_native('nameWithoutExtension')

    @property
    def newest_document_date(self) -> Optional[str]:
        """Newest date extracted from text of document, e.g. a scan."""
        return self.get_property_native('newestDocumentDate')

    @property
    def number_of_duplicates(self) -> int:
        """The number of duplicates of a record."""
        return self.get_property_native('numberOfDuplicates')

    @property
    def number_of_hits(self) -> int:
        """The number of hits of a record."""
        return self.get_property_native('numberOfHits')

    @number_of_hits.setter
    def number_of_hits(self, value: int):
        self.set_property('numberOfHits', value)

    @property
    def number_of_replicants(self) -> int:
        """The number of replicants of a record."""
        return self.get_property_native('numberOfReplicants')

    @property
    def oldest_document_date(self) -> Optional[str]:
        """Oldest date extracted from text of document, e.g. a scan."""
        return self.get_property_native('oldestDocumentDate')

    @property
    def opening_date(self) -> Optional[str]:
        """Date when a content was opened the last time or when a feed was refreshed the last time."""
        return self.get_property_native('openingDate')

    @property
    def page_count(self) -> int:
        """The page count of a record. Currently only supported by PDF documents."""
        return self.get_property_native('pageCount')

    @property
    def paginated_pdf(self):
        """A printed/converted PDF of the record."""
        return self.get_property_native('paginatedPDF')

    @property
    def path(self) -> str:
        """The POSIX file path of a record. Only the path of external records can be changed."""
        return self.get_property_native('path')
    
    @path.setter
    def path(self, value: str):
        self.set_property('path', value)

    @property
    def pending(self) -> bool:
        """Flag whether the (latest) contents of a record haven't been downloaded from a sync location yet."""
        return self.get_property_native('pending')

    @property
    def plain_text(self) -> str:
        """The plain text of a record."""
        return self.get_property_native('plainText')
    
    @plain_text.setter
    def plain_text(self, value: str):
        self.set_property('plainText', value)

    @property
    def proposed_filename(self) -> str:
        """The proposed filename for a record."""
        return self.get_property_native('proposedFilename')

    @property
    def rating(self) -> int:
        """Rating (0-5) of a record."""
        return self.get_property_native('rating')

    @rating.setter
    def rating(self, value: int):
        self.set_property('rating', value)

    @property
    def reference_url(self) -> str:
        """The URL (x-devonthink-item://...) to reference/link back to a record.
        Append ?page= to specify the zero-based index of a page of a PDF document,
        ?time= to specify the time of a movie or ?search= to specify a string to search.
        """
        return self.get_property_native('referenceURL')

    @property
    def reminder(self) -> Optional['Reminder']:
        """Reminder of a record."""
        return self.get_property_native('reminder')

    @reminder.setter
    def reminder(self, value: 'Reminder'):
        self.set_property('reminder', value)

    @property
    def rich_text(self) -> Optional[str]:
        """The rich text of a record (see text suite). 
        Use the 'text' relationship introduced by version 3.0 instead,
        especially for changing the contents/styles of RTF(D) documents."""
        return self.get_property_native('richText')

    @property
    def score(self) -> float:
        """The score of the last comparison, classification or search (value between 0.0 and 1.0) or undefined otherwise."""
        return self.get_property_native('score')

    @property
    def size(self) -> int:
        """The size of a record in bytes."""
        return self.get_property_native('size')

    @property
    def source(self) -> str:
        """The HTML/XML source of a record if available or the record converted to HTML if possible."""
        return self.get_property_native('source')

    @property
    def state(self) -> bool:
        """The state/flag of a record."""
        return self.get_property_native('state')

    @state.setter
    def state(self, value: bool):
        self.set_property('state', value)

    @property
    def state_visibility(self) -> bool:
        """Obsolete."""
        raise NotImplementedError()

    @property
    def tag_type(self) -> str:
        """The tag type of a record."""
        return self.get_property_native('tagType')

    @property
    def tags(self) -> List[str]:
        """The tags of a record."""
        return self.get_property_native('tags')

    @tags.setter
    def tags(self, value: list):
        self.set_property('tags', value)

    @property
    def thumbnail(self) -> Optional[str]:
        """The thumbnail of a record. Setting supports both raw data and strings containing paths or URLs."""
        return self.get_property_native('thumbnail')

    @thumbnail.setter
    def thumbnail(self, value: any):
        self.set_property('thumbnail', value)

    @property
    def type(self) -> str:
        """
        The type of a record. ("bookmark"/‌"feed"/‌"formatted note"/‌"group"/‌"html"/‌"markdown"/‌"PDF document"/‌"picture"/‌"plist"/‌"quicktime"/‌"rtf"/‌"rtfd"/‌"script"/‌"sheet"/‌"smart group"/‌"txt"/‌"unknown"/‌"webarchive"/‌"xml")
        Note: In compiled menu/toolbar scripts you might have to use a string representation of the type for comparisons.
        """
        return self.get_property_native('type')

    @property
    def unread(self) -> bool:
        """The unread flag of a record."""
        return self.get_property_native('unread')

    @unread.setter
    def unread(self, value: bool):
        self.set_property('unread', value)

    @property
    def url(self) -> str:
        """The URL of a record."""
        return self.get_property_native('url')

    @property
    def uuid(self) -> str:
        """The unique and persistent identifier of a record."""
        return self.get_property_native('uuid')

    @property
    def web_archive(self):
        """The web archive of a record if available or the record converted to web archive if possible."""
        return self.get_property_native('webArchive')

    @property
    def width(self) -> int:
        """The width of an image or PDF document in pixels."""
        return self.get_property_native('width')

    @property
    def word_count(self) -> int:
        """The word count of a record."""
        return self.get_property_native('wordCount')
    
    def __repr__(self):
        return f'<Record: {self.name}>'

OSAObjProxy._NAME_CLASS_MAP['record'] = Record
OSAObjProxy._NAME_CLASS_MAP['content'] = Record
OSAObjProxy._NAME_CLASS_MAP['parent'] = Record
OSAObjProxy._NAME_CLASS_MAP['child'] = Record
OSAObjProxy._NAME_CLASS_MAP['selectedRecord'] = Record