from typing import Iterable, List

from pyaltium.magicstrings import SchematicPinType

COUNT = 0


def byte_arr_str(s: bytes) -> bytes:
    """Get a string encoded in a byte array."""
    size = s[0]
    name = s[1 : size + 1]
    print(f"{size}: {name}")
    return name, s[size + 1 :]


def pinstr_to_records(s: bytes) -> List[dict]:
    """Actually take a pin string and turn it into usable records."""
    records = []

    global COUNT

    rotations = {0: 0, 1: 90, 2: 180, 3: 270}
    count1 = 0
    orig = s

    while True:
        COUNT += 1
        count1 += 1
        if COUNT >= 5:
            print("stop!")
            pass
        try:
            if not len(s) > 10:
                break

            record = {}
            # Trim beginning of string
            OLD = s
            s = s[17:]
            description, s = byte_arr_str(s)
            print(f"description: {description}")

            if description:
                record["DESCRIPTION"] = description

            record["TYPE"] = SchematicPinType(int.from_bytes(s[1:2], "big"))

            rot_hide = int.from_bytes(s[2:3], "big")
            record["ROTATION"] = rotations[rot_hide & 0x03]

            record["HIDE_DESIGNATOR"] = bool(rot_hide & 0x08)
            record["HIDE_NAME"] = bool(rot_hide & 0x10)
            record["PINLENGTH"] = int.from_bytes(s[3:4], "big") * 10
            record["LOCATION.X"] = int.from_bytes(s[4:6], "big", signed=True) * 10
            record["LOCATION.Y"] = int.from_bytes(s[6:8], "big", signed=True) * 10

            s = s[13:]
            record["NAME"], s = byte_arr_str(s)
            record["DESIGNATOR"], s = byte_arr_str(s)

            rn = record["NAME"]
            rd = record["DESIGNATOR"]
            print(f"n:d is {rn}:{rd}")

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

            # Remove non-alphanumeric from the key, sometimes things are wonky
            # rec[key] = b"".join(filter(str.isalnum, newval))

            # If it's too short to be a pin, it's probably just junk so ignore
            if len(pinstr) > 20:
                print("UPDATING RECORD")
                # print(rec)
                complete_str = b"\x00" + pinstr
                newrecords.extend(pinstr_to_records(complete_str))

        retlist.append(rec)
        retlist.extend(newrecords)

    return retlist
