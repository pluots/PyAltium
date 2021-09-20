"""helpers.py"""


def altium_string_split(s: str) -> list:
    """Just split into a list by the pipe character"""
    return s.split('|')


def altium_value_from_key(arr: list, key: str) -> str:
    """Loop through """
    for item in arr:
        if item.startswith(key):
            return item.replace(key+'=','')

    # Just return empty if not found
    return ''


def sch_sectionkeys_to_list(arr: list) -> dict:
    """
    Turn sectionkeys into a list with the form:
    {
        libref1: sectionkey
        libref2: sectionkey
    }
    """
    key_count = int(altium_value_from_key(arr, 'KeyCount'))

    retdict = {}

    for i in range(0, key_count - 1):
        retdict[altium_value_from_key(arr, 'LibRef' + str(i))] \
            = altium_value_from_key(arr, 'SectionKey' + str(i))

    return retdict
