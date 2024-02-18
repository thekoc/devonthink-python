To convert the JXA (JavaScript for Automation) file to Python code, you should follow a structured approach. Here's a guide on how to interpret and translate JXA definitions into Python classes, properties, and methods:

### Python Class Translation

1. **Class Name and Description**: Convert the JXA object name to a Python class name, and use the JXA description as a docstring.

2. **Elements**: Elements are read-only properties in Python. Use `@property` decorator to define getters.

3. **Properties**: Convert JXA properties to Python properties. Use `@property` for getters. For read-write properties, add a `@property.setter` decorator. Note that if the return type is primitive (like `text`, `integer`, `real`, etc.), you should use `_call_method` not `_get_property` in getter.

4. **Methods**: Methods should be converted into Python class methods. Arguments with square brackets are optional.

5. **Positional versus Keyword Arguments**: When translating JXA methods to Python, it’s essential to accurately determine whether arguments are positional or keyword arguments. In JXA definition, if the argument has both name and type (eg. (newline) record: Record : <description>) then it is a keyword argument in Python. If the argument is listed on the same line as the method name, without an explicit name, (`<method_name>` Record: <description>) it is a positional argument in Python.

    Example:
    1. consolidate method : Move an external/indexed record (and its children) into the database.
    consolidate
    record: Record : The record to consolidate.
    → boolean

    In this case, `record` is a keyword argument in Python.

    2. consolidate method : Move an external/indexed record (and its children) into the database.
    consolidate Record: The record to consolidate.
    → boolean

    In this case, `Record` is a positional argument in Python.

6. **Naming Conventions**: Convert camelCase names from JXA to snake_case in Python.

### Example Conversion

#### JXA Definition

```txt
Mailbox Object, pl mailboxes : A mailbox that holds messages
elements
contains mailboxes, messages; contained by application, accounts, mailboxes.
properties
name (text) : The name of a mailbox
unreadCount (integer, r/o) : The number of unread messages in the mailbox
account (Account, r/o)
```

#### Python Code

```python
class Mailbox(OSAObjProxy):
    """A mailbox that holds messages."""
    # ========== Elements ==========
    @property
    def mailboxes(self) -> OSAObjArray[Mailbox]: # Note that you should use OSAObjArray for lists of objects
        return self._get_property('mailboxes')
    
    @property
    def messages(self) -> OSAObjArray[Message]:
        return self._get_property('messages')
    
    # ========== Properties ==========
    @property
    def name(self) -> str:
        """The name of a mailbox."""
        return self._call_method('name')
    
    @name.setter
    def name(self, value: str):
        self._set_property('name', value)

    @property
    def unread_count(self) -> int:
        """The number of unread messages in the mailbox."""
        return self._call_method('unreadCount')
    
    @property
    def account(self) -> Account:
        """The account that the mailbox belongs to."""
        return self._get_property('account')
```

#### JXA Methods Definition

```txt
createLocation method : Create a hierarchy of groups if necessary.
createLocation Text : The hierarchy as a POSIX path (/ in names has to be replaced with \/, see location property).
[in: Database] : The database. Uses current database if not specified.
→ Record
addReadingList method : Add record or URL to reading list.
addReadingList
[record: Record] : The record. Only documents are supported.
[title: Text] : The title of the webpage.
[url: Text] : The URL of the webpage.
→ boolean
addRow method : Add new row to current sheet.
addRow specifier : the object for the command
[cells: list] : Cells of new row.
→ boolean
```

#### Python Methods

```python
def create_location(self, path: str, database: Database = None) -> Record:
    """Create a hierarchy of groups if necessary.

    Args:
        path (str): The hierarchy as a POSIX path (/ in names has to be replaced with \/, see location property).
        database (Database, optional): The database. Uses current database if not specified.

    Returns:
        Record: The created record.
    """
    kwargs = {
        'in': database
    }
    return self._call_method('createLocation', args=[path], kwargs={k: v for k, v in kwargs.items() if v is not None}

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
    return self._call_method('addReadingList', args=[], kwargs={k: v for k, v in kwargs.items() if v is not None})

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
```
**Important: When converting method, please ensure the rule 5 (Positional versus Keyword Arguments) is followed.**


This approach should be applied to all objects, properties, and methods in the JXA file to create their corresponding Python counterparts.

When converting, just output the methods and properties of the class. Do not include the class definition or any imports.

Before you output, think carefully and double check whether each argument should be positional or keyword.

If you understood, reply "Ready" and I'll send you a sdef file. Respond with python code and nothing else.
