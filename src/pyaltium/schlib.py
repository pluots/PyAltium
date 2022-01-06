

from pyaltium.base import AltiumFileType
from pyaltium.helpers import (
    altium_string_split,
    altium_value_from_key,
    sch_sectionkeys_to_dict,
)
from pyaltium.magicstrings import SCHLIB_HEADER


class SchLib(AltiumFileType):
    """Main object to interact with schematic libraries."""

    def _verify_file_type(self, fname: str) -> bool:
        """Check if our magic string is in the header."""
        fh_str = self._read_decode_stream("FileHeader", 128)
        return SCHLIB_HEADER in fh_str

    def _update_header_and_section_keys(self) -> None:
        """Just update class's _header_dict object."""
        fh_str = self._read_decode_stream("FileHeader")
        sk_str = self._read_decode_stream("SectionKeys")

        self._header_dict = altium_string_split(fh_str)
        self._section_keys_list = altium_string_split(sk_str)

    def _update_item_list(self) -> None:
        """Override main class, just update the list of items in the library.

        Most of this information is kept in the file header. However, we need
        to get some information from sectionkeys if names got truncated in the header.
        """
        d = self._header_dict

        # Get the component count so we know what to look for
        item_count = int(altium_value_from_key(d, "CompCount"))

        self._items_list = []

        sec_keys = sch_sectionkeys_to_dict(self._section_keys_list)

        # Loop through each item listed in the fileheader
        for i in range(0, item_count - 1):
            libref = altium_value_from_key(d, "LibRef" + str(i))
            description = altium_value_from_key(d, "CompDescr" + str(i))
            partcount = int(altium_value_from_key(d, "PartCount" + str(i))) - 1

            if libref in sec_keys:
                sectionkey = sec_keys[libref]
            else:
                sectionkey = libref

            self._items_list.append(
                {
                    "libref": libref,
                    "description": description,
                    "partcount": partcount,
                    "sectionkey": sectionkey,
                }
            )

    def list_items(self) -> list:
        return self._items_list


# class SchLibItem():
#     def __init__(self):
#         pass

# def __respr__(self):
#     pass
