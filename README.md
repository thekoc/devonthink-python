# PyDT3 - The Python API For DEVONthink 3

This Python API for Devonthink 3 utilizes AppleScript (JXA) and PyObjC.

The Applescript bridging part is inspired by [py-applescript](https://github.com/rdhyee/py-applescript).

## Installation

```bash
pip install pydt3
```

## Quick Start

```python
from pydt3 import DEVONthink3
dt3 = DEVONthink3()
for db in dt3.databases:
    print(db.name)
```

## Requirements

- DEVONthink 3
- Python 3.6+
- PyObjC

## Documentation

See docstrings in codes. The API maps to the AppleScript API as closely as possible.

## Limitations

- The APIs are not fully tested. Please report any issues.
- Rich texts in AppleScript are converted to strings in Python, which causes style information loss.
- Collections of elements (eg. `database.records`) are converted to lists in Python. While in Applescript they are lazily retrieved. This may cause performance issues with large collection.
