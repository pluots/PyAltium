"""magicstrings.py"""
from enum import IntEnum, unique
from typing import Union

SCHLIB_HEADER = (
    "HEADER=Protel for Windows - Schematic Library Editor Binary File Version 5.0"
)
PCBLIB_HEADER = "PCB 6.0 Binary Library File"
MAX_READ_SIZE_BYTES = 1024 * 1024


@unique
class SchematicRecordType(IntEnum):
    """These types are stored in a schematic file."""

    UNDEFINED = 0
    COMPONENT = 1
    PIN = 2
    IEEE_SYMBOL = 3
    LABEL = 4
    BEZIER = 5
    POLYLINE = 6
    POLYGON = 7
    ELLIPSE = 8
    PIECHART = 9
    RECTANGLE_ROUND = 10
    ELIPTICAL_ARC = 11
    ARC = 12
    LINE = 13
    RECTANGLE = 14
    SHEET_SYMBOL = 15
    SHEET_ENTRY = 16
    POWER_PORT = 17
    PORT = 18
    NO_ERC = 22
    NET_LABEL = 25
    BUS = 26
    WIRE = 27
    TEXT_FRAME = 28
    JUNCTION = 29
    IMAGE = 30
    SHEET = 31
    SHEET_NAME = 32
    FILE_NAME = 33
    DESIGNATOR = 34
    BUS_ENTRY = 37
    TEMPLATE = 39
    PARAMETER = 41
    IMPLEMENTATION_LIST = 44


@unique
class SchematicPinType(IntEnum):
    """Possible types for a pin."""

    INPUT = 0
    IO = 1
    OUTPUT = 2
    OPEN_COLLECTOR = 3
    PASSIVE = 4
    HIGH_Z = 5
    OPEN_EMITTER = 6
    POWER = 7


def get_sch_record(value: Union[str, int]):
    try:
        if isinstance(value, str):
            return SchematicRecordType(int(value))
        return SchematicRecordType(value)
    except ValueError:
        return SchematicRecordType(0)
