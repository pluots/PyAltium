from enum import IntEnum, unique
from typing import Dict, List, Tuple, Union

from pyaltium._helpers import byte_arr_str


@unique
class SchLibItemRecordType(IntEnum):
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
class SchPinType(IntEnum):
    """Possible types for a pin."""

    INPUT = 0
    IO = 1
    OUTPUT = 2
    OPEN_COLLECTOR = 3
    PASSIVE = 4
    HIGH_Z = 5
    OPEN_EMITTER = 6
    POWER = 7


PinRecType = Dict[str, Union[bytes, int, SchLibItemRecordType]]

_rotations = {0: 0, 1: 90, 2: 180, 3: 270}


def pinstr_worker(s_in: bytes) -> Tuple[PinRecType, str]:

    record: PinRecType = {}

    # Trim beginning of string
    s = s_in[17:]
    description, s = byte_arr_str(s)

    if description:
        record["Description"] = description

    record["PinType"] = SchPinType(int.from_bytes(s[1:2], "little"))

    rot_hide = int.from_bytes(s[2:3], "little")
    record["Rotation"] = _rotations[rot_hide & 0x03]
    record["Hide_Designator"] = bool(rot_hide & 0x08)
    record["Hide_Name"] = bool(rot_hide & 0x10)

    record["PinLength"] = int.from_bytes(s[3:5], "little") * 10
    record["Location.X"] = int.from_bytes(s[5:7], "little", signed=True)
    record["Location.Y"] = int.from_bytes(s[7:9], "little", signed=True)

    s = s[13:]
    record["Name"], s = byte_arr_str(s)
    record["Designator"], s = byte_arr_str(s)
    s = s[5:]
    return record, s


def pinstr_to_records(s: bytes) -> List[PinRecType]:
    """Actually take a pin string and turn it into usable records."""
    records: List[PinRecType] = []

    while True:
        try:
            if not len(s) > 10:
                break

            record, s = pinstr_worker(s)
            record["RECORD"] = SchLibItemRecordType.PIN
            records.append(record)
        except IndexError:
            pass

    return records
