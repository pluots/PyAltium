from pyaltium.base import AltiumLibMixin
from pyaltium.helpers import (
    altium_string_split,
    altium_value_from_key,
    sch_sectionkeys_to_dict,
)
from pyaltium.magic import SCHLIB_HEADER
from pyaltium.sch.libitem import SchLibItem


class SchLib(AltiumLibMixin[SchLibItem]):
    """Main object to interact with schematic libraries."""

    def __init__(self, file_name: str = None, lazyload: bool = False) -> None:
        """A schematic library representation.

        :param file_name: [description], defaults to None
        :type file_name: str, optional
        :param lazyload: [description], defaults to False
        :type lazyload: bool, optional
        """
        super().__init__(file_name=file_name, lazyload=lazyload)

    def _verify_file_type(self, fname: str) -> bool:
        """Check if our magic string is in the header."""
        fh_str = self._read_decode_stream("FileHeader", 128)
        return SCHLIB_HEADER in fh_str

    def _update_header_and_section_keys(self) -> None:
        """Just update class's _header_keys_list object."""
        fh_str = self._read_decode_stream("FileHeader")
        sk_str = self._read_decode_stream("SectionKeys")

        self._header_keys_list = altium_string_split(fh_str)
        self._section_keys_list = altium_string_split(sk_str)

    def _update_item_list(self) -> None:
        """Override main class, just update the list of items in the library.

        Most of this information is kept in the file header. However, we need
        to get some information from sectionkeys if names got truncated in the header.
        """
        d = self._header_keys_list

        # Get the component count so we know what to look for
        item_count = int(altium_value_from_key(d, "CompCount"))

        self.items_list = []

        sec_keys = sch_sectionkeys_to_dict(self._section_keys_list)

        # Loop through each item listed in the fileheader
        for i in range(item_count):
            libref = altium_value_from_key(d, f"LibRef{i}")
            description = altium_value_from_key(d, f"CompDescr{i}")
            partcount = int(altium_value_from_key(d, f"PartCount{i}")) - 1

            if libref in sec_keys:
                sectionkey = sec_keys[libref]
            else:
                sectionkey = libref

            self.items_list.append(
                SchLibItem(
                    libref=libref,
                    description=description,
                    partcount=partcount,
                    sectionkey=sectionkey,
                    file_name=self.file_name,
                )
            )
