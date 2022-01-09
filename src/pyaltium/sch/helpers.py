from enum import IntEnum, unique
from typing import Dict, List, Union

from pyaltium.helpers import byte_arr_str


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


def pinstr_to_records(s: bytes) -> List[dict]:
    """Actually take a pin string and turn it into usable records."""
    records = []

    rotations = {0: 0, 1: 90, 2: 180, 3: 270}

    while True:
        try:
            if not len(s) > 10:
                break

            record: Dict[str, Union[bytes, int, SchLibItemRecordType]] = {
                "RECORD": SchLibItemRecordType.PIN
            }
            # Trim beginning of string
            s = s[17:]
            description, s = byte_arr_str(s)

            if description:
                record["Description"] = description

            record["PinType"] = SchPinType(int.from_bytes(s[1:2], "big"))

            rot_hide = int.from_bytes(s[2:3], "big")
            record["Rotation"] = rotations[rot_hide & 0x03]

            record["Hide_Designator"] = bool(rot_hide & 0x08)
            record["Hide_Name"] = bool(rot_hide & 0x10)
            record["PinLength"] = int.from_bytes(s[3:4], "big") * 10
            record["Location.X"] = int.from_bytes(s[4:6], "big", signed=True)
            record["Location.Y"] = int.from_bytes(s[6:8], "big", signed=True)

            s = s[13:]
            record["Name"], s = byte_arr_str(s)
            record["Designator"], s = byte_arr_str(s)

            records.append(record)

            s = s[5:]

        except IndexError:
            pass

    return records
