# PyAltium

NOTE: This tool is currently broken and incomplete, and is awaiting a rewrite!

A tool to process Altium file types. Currently this tool is in alpha and does not have any parts fully functioning, except for the listing of PCBLib and SCHLib libraries.

See full documentation here (WIP): [pyaltium.readthedocs.io](http://pyaltium.readthedocs.io)

## Project Progress

The goal of this project is to support most file types used by Altium. Reading is a priority, writing will be implemented for some types. The status of various file types is listed below:

|                          | Extension   | List Items | Display | Write | Documentation                         |
| ------------------------ | ----------- | ---------- | ------- | ----- | ------------------------------------- |
| Binary Schematic Library | .SchLib     | ✓          | WIP     |       | WIP                                   |
| Binary PCB Library       | .PcbLib     | ✓          | WIP     |       | WIP                                   |
| Binary Schematic Doc     | .SchDoc     |            |         |       |                                       |
| Binary PCB Doc           | .PcbDoc     |            |         |       |                                       |
| Draftsman Doc            | .PcbDwf     |            |         |       |                                       |
| PCB Project              | .PrjPcb     |            |         |       |                                       |
| Material Library         | .xml        | ✓          | N/A     | ✓     | WIP (see test_matlib in the meantime) |
| Any templates            | Not Planned |            |         |       |                                       |

## Usage

### SchLib

Sample usage:

```python
import pprint
from pyaltium import SchLib

# Set up our pretty printer so our output is understandable
pp = pprint.PrettyPrinter(indent=4)

sl = SchLib("myfile_name.SchLib")
pp.pprint(SchLib.list_items())
```

This returns something like the following with more elements:

```JSON
[
    {
        "libref": "ref1",
        "description": "My description",
        "sectionkey": "Section Key" // This is unneeded, just for internals
    }
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

sl = SchLib("myfile_name.SchLib")
pp.pprint(SchLib.list_items())
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

## Contributing

Have an idea? Open an issue! Have a change? submit a PR!

Note that I have a long ways to go on this so don't expect too much as of now.
Help is always welcome.

## Licensing

This project is licensed under GPLv3. Basically you can use this however you
want but if you distribute (aka sell) something with it, you need to make
the source available. Once this project gains some traction, I'll be open to
moving to MIT if there's demand for it.
