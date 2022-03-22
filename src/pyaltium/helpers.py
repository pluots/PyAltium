"""helpers.py"""
import re
from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal
from typing import Any, AnyStr, Literal, Tuple, Union
from uuid import UUID

import olefile

from pyaltium.magic import MAX_READ_SIZE_BYTES

REALNUM = Union[int, float]

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
    s: bytes, len_length: int = 1, endianness: Literal["little", "big"] = "little"
) -> Tuple[str, bytes]:
    """Get a string encoded in a byte array.

    s is the string for data to be extracted from.
    len_length is the length of the length indicator
    at the start of the string."""
    len_text = int.from_bytes(s[0:len_length], endianness)
    text_end = len_length + len_text
    text = s[len_length:text_end]
    return text.decode("utf8"), s[text_end:]


def mil_to_um(n):
    pass


def humanize(val: REALNUM, unit: str = "", space=True, trim=True, quantize=None) -> str:
    def quant(d):
        if trim:
            d = d.quantize(Decimal(1)) if d == d.to_integral() else d.normalize()
        if not quantize:
            return str(d)
        return d.quantize(Decimal(str(quantize)), rounding=ROUND_HALF_UP)

    if space:
        space = " "
    else:
        space = ""

    val = Decimal(val)

    if val < 1000:
        return f"{quant(val)}{space}{unit}"
    if val < 1000 ** 2:
        return f"{quant(val/1000)}{space}k{unit}"
    if val < 1000 ** 3:
        return f"{quant(val/(1000**2))}{space}M{unit}"
    if val < 1000 ** 4:
        return f"{quant(val/(1000**3))}{space}G{unit}"
    return f"{quant(val/(1000**4))}{space}T{unit}"


def dehumanize(s: str, unit: str = "") -> Decimal:
    res = re.search(r"(\d+\.?\d*)(\w*)", s)
    num = res.group(1)
    sfx = res.group(2)

    sfx.strip()
    if unit:
        sfx = sfx.replace(unit, "")

    d = Decimal(num)
    if sfx.startswith("k"):
        return d * 1000
    if sfx.startswith("M"):
        return d * 1000 ** 2
    if sfx.startswith("G"):
        return d * 1000 ** 3
    if sfx.startswith("T"):
        return d * 1000 ** 4
    return d


def safe_uuid(*args, ret="input", **kwargs):
    """Return a UUID even when input is corruptable.

    ret sets what to return when failed. "input" returns input as given."""
    try:
        return UUID(*args, **kwargs)
    except (TypeError, ValueError):
        if ret == "input":
            if len(args) > 1:
                return args[0]
            return kwargs.get("int", kwargs.get("hex"))
        return UUID(int=0)


def load_dt(s: str):
    s = s.replace("Z", "+00:00")
    return datetime.fromisoformat(s.replace("Z", "+00:00"))
