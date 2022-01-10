"""helpers.py"""
import re
from typing import Any, AnyStr, Literal, Tuple

import olefile

from pyaltium.magic import MAX_READ_SIZE_BYTES

re_before_first_record = re.compile(r"^.*?(\|RECORD)")
re_cleanstr = re.compile(r"[^\w_\.]")

# Ignore |& bridges, like for pin records
re_split_exclude_ampersand = re.compile(r"\|(?<!\|&)")


def altium_string_split(s: AnyStr) -> list:
    """Just split into a list by the pipe character"""
    split = "|" if isinstance(s, str) else b"|"
    return s.split(split)


def altium_value_from_key(arr: list, key: str) -> str:
    """Find a key in an altium string, return its value."""
    for item in arr:
        if item.startswith(key):
            return item.replace(f"{key}=", "")

    # Just return empty if not found
    return ""


def sch_sectionkeys_to_dict(arr: list) -> dict:
    """
    Turn sectionkeys into a dict with the form:
    {
        libref1: sectionkey
        libref2: sectionkey
    }
    """
    key_count = altium_value_from_key(arr, "KeyCount")
    if len(key_count) == 0:
        key_count = "0"

    key_count_int = int(key_count)

    retdict = {}

    for i in range(0, key_count_int - 1):
        retdict[altium_value_from_key(arr, f"LibRef{str(i)}")] = altium_value_from_key(
            arr, f"SectionKey{str(i)}"
        )

    return retdict


def read_decode_stream(
    filename: str, streamname: str, readbytes: int = MAX_READ_SIZE_BYTES
) -> str:
    """Read a stream (in one go) and decode it. Maybe add yield in the future."""
    with olefile.OleFileIO(filename) as ole:
        try:
            stream = ole.openstream(streamname)
            return stream.read(readbytes).decode("utf8")
        except OSError:
            # Can't find stream
            return ""


def eval_bool(b: str) -> bool:
    """Evaluate possible bool values"""
    return b.lower() in ("1", "t", "true")


def eval_color(c: int = None) -> str:
    """Fix the dumb color flip flop."""
    if not c:
        return "#FFFFFF"
    r = c & 0x0000FF
    g = (c & 0x00FF00) >> 8
    b = (c & 0xFF0000) >> 16

    return f"#{r:02x}{g:02x}{b:02x}"


def normalize_value(x: Any, key: bool = False):
    """Handle a single value in a dict"""
    if not isinstance(x, bytes):
        return x
    s = re_cleanstr.sub("", x.decode("utf8", "ignore"))

    # Keys will always be strings, try to convert any values
    if not key:
        try:
            return int(s)
        except ValueError:
            pass
        try:
            return float(s)
        except ValueError:
            pass
    return s


def normalize_dict(d: dict) -> dict:
    """Decode dictionary key/values and remove extra binary characters."""

    return {
        normalize_value(k, key=True): normalize_value(v)
        for k, v in d.items()
        if k and v
    }


def byte_arr_str(
    s: bytes, len_length: int = 1, endianness: Literal["little", "big"] = "big"
) -> Tuple[bytes, bytes]:
    """Get a string encoded in a byte array.

    s is the string for data to be extracted from.
    len_length is the length of the length indicator
    at the start of the string."""
    len_text = int.from_bytes(s[0:len_length], endianness)
    text_end = len_length + len_text
    text = s[len_length:text_end]
    return text, s[text_end:]


def mil_to_um(n):
    pass
