# PyAltium

A tool to process Altium file types. Currently only supports reading of .SchLib and
.PcbLib files.

See full documentation here: [pyaltium.readthedocs.io](pyaltium.readthedocs.io)

### SchLib

Sample usage:

```python
import pprint
from pyaltium import SchLib

# Set up our pretty printer so our output is understandable
pp = pprint.PrettyPrinter(indent=4)

sl = SchLib('myfile_name.SchLib')
print(SchLib.list_items())

```

Returns

```JSON
[
    {
        "libref": "ref1",
        "description": "My description",
        "sectionkey": "Section Key" // This is unneeded, just for internals
    },
    // ...
]
```

### PCBLib

Currently the only PCB library capability is creating a list of footprints

Sample usage:

```python
import pprint
from pyaltium import SchLib

# Set up our pretty printer so our output is understandable
pp = pprint.PrettyPrinter(indent=4)

sl = SchLib('myfile_name.SchLib')
print(SchLib.list_items())

```

Returns:

```JSON
[
    {
        "footprintref": "ref1",
        "height": "2.8", // mm
        "description": "My description"
    },
    // ...
]
```
