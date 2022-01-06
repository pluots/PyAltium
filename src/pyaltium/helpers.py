"""helpers.py"""


def altium_string_split(s: str) -> list:
    """Just split into a list by the pipe character"""
    return s.split("|")


def altium_value_from_key(arr: list, key: str) -> str:
    """Loop through and replace "key" part."""
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
    if key_count == "":
        key_count = 0
    else:
        key_count = int(key_count)

    retdict = {}

    for i in range(0, key_count - 1):
        retdict[altium_value_from_key(arr, f"LibRef{str(i)}")] = altium_value_from_key(
            arr, f"SectionKey{str(i)}"
        )

    return retdict
