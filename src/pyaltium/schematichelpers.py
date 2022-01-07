from typing import Iterable, List

from pyaltium.magicstrings import SchematicPinType, SchematicRecordType


def byte_arr_str(s: bytes) -> bytes:
    """Get a string encoded in a byte array."""
    size = s[0]
    name = s[1 : size + 1]
    return name, s[size + 1 :]


def pinstr_to_records(s: bytes) -> List[dict]:
    """Actually take a pin string and turn it into usable records."""
    records = []

    rotations = {0: 0, 1: 90, 2: 180, 3: 270}

    while True:
        try:
            if not len(s) > 10:
                break

            record = {"RECORD": SchematicRecordType.PIN}
            # Trim beginning of string
            s = s[17:]
            description, s = byte_arr_str(s)

            if description:
                record["Description"] = description

            record["PinType"] = SchematicPinType(int.from_bytes(s[1:2], "big"))

            rot_hide = int.from_bytes(s[2:3], "big")
            record["Rotation"] = rotations[rot_hide & 0x03]

            record["Hide_Designator"] = bool(rot_hide & 0x08)
            record["Hide_Name"] = bool(rot_hide & 0x10)
            record["PinLength"] = int.from_bytes(s[3:4], "big") * 10
            record["Location.X"] = int.from_bytes(s[4:6], "big", signed=True) * 10
            record["Location.Y"] = int.from_bytes(s[6:8], "big", signed=True) * 10

            s = s[13:]
            record["Name"], s = byte_arr_str(s)
            record["Designator"], s = byte_arr_str(s)

            records.append(record)

            s = s[5:]

        except IndexError:
            pass

    return records


def handle_pin_records(records: Iterable[dict]) -> list:
    """Run through a list of records for a schematic component and handle pins.

    Pins are a bit weird. There is no record type for them so they are just binary
    strings in the middle of other textual records.

    That means we need to go through all the records and explicitely split this off,
    since they just tag along with whatever record preceeded them.


    |
    """

    retlist = []

    for rec in records:
        newrecords = []
        for key, val in rec.items():
            # If there is nothing bytes in the string, we are set
            if b"\x00" not in val:
                continue

            # Otherwise, do cleanup
            newval, pinstr = val.split(b"\x00", 1)
            rec[key] = newval

            # If it's too short to be a pin, it's probably just junk so ignore
            if len(pinstr) > 20:
                # print(rec)
                complete_str = b"\x00" + pinstr
                newrecords.extend(pinstr_to_records(complete_str))

        retlist.append(rec)
        retlist.extend(newrecords)

    return retlist
