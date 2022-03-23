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


def to_um(n) -> Decimal:
    """Coerce a string with units to mm

    :param s: String to format
    :type s: str
    :return: Decimal version of the given string
    :rtype: Decimal
    """


def to_mm(s: str) -> Decimal:
    """Coerce a string with units to mm

    :param s: String to format
    :type s: str
    :return: Decimal version of the given string in mm
    :rtype: Decimal
    """
    if "mil" in s:
        return Decimal(s.replace("mm", "")) * Decimal(0.0254)
    if "in" in s or "inch" in s or '"' in s:
        return Decimal(
            s.replace("inch", "").replace("in", "").replace('"', "")
        ) * Decimal(25.4)

    # Assume mm by default
    return Decimal(s.replace("mm", ""))


def to_celsius(s: str) -> Decimal:
    """Coerce a string with units to Celsius

    :param s: String to format
    :type s: str
    :return: Decimal version of the given string in °C
    :rtype: Decimal
    """

    s = s.replace("°", "")

    if "F" in s:
        return (Decimal(s.replace("F", "")) - Decimal(32)) * Decimal(5 / 9)
    if "K" in s:
        return Decimal(s.replace("K", "")) - Decimal(273.15)
    # Assume C by default
    return Decimal(s.replace("C", ""))


def humanize(
    val: REALNUM,
    unit: str = "",
    space=False,
    trim=True,
    quantize=None,
    prefix=True,
    baseunit: str = None,
    rounding=ROUND_HALF_UP,
) -> str:
    """Humanize a value to SI units.

    :param val: Value to humanize
    :type val: REALNUM
    :param unit: Unit to append at the end ('Hz', 'm', etc), defaults to ""
    :type unit: str, optional
    :param space: Whether to include a space between the number and the unit, defaults to True
    :type space: bool, optional
    :param trim: Whether to remove trailing zeroes within given quantization, defaults to True
    :type trim: bool, optional
    :param quantize: Quantize specification for rounding if desired, e.g. '0.01', defaults to None
    :type quantize: _type_, optional
    :return: Formatted string
    :rtype: str
    """

    def quant(d):
        # If we quantize,
        if quantize:
            d = d.quantize(Decimal(str(quantize)), rounding=rounding)

        if trim:
            # Check if decimal is an int; if so, use quantize
            # Normalize will set e.g. 100 to '1E+2'
            if d == d.to_integral():
                d = d.quantize(Decimal(1))
            # Otherwise use normalize to remove trailing zeroes
            else:
                d = d.normalize()
        return str(d)

    if space:
        space = " "
    else:
        space = ""

    val = Decimal(val)

    if baseunit:
        raise NotImplementedError

    if not prefix or val < 1000:
        return f"{quant(val)}{space}{unit}"
    if val < 1000 ** 2:
        return f"{quant(val/1000)}{space}k{unit}"
    if val < 1000 ** 3:
        return f"{quant(val/(1000**2))}{space}M{unit}"
    if val < 1000 ** 4:
        return f"{quant(val/(1000**3))}{space}G{unit}"
    return f"{quant(val/(1000**4))}{space}T{unit}"


def dehumanize(s: str, unit: str = "") -> Decimal:
    """Remove SI units and return the equivilent decimal.

    :param s: String to format
    :type s: str
    :param unit: Base unit to work with (e.g. "Hz", "m"), defaults to ""
    :type unit: str, optional
    :return: Decimal format of the returned value
    :rtype: Decimal
    """
    # Get units
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
