import olefile

from pyaltium.base import AltiumLibraryItemType, AltiumLibraryType
from pyaltium.helpers import altium_string_split, altium_value_from_key
from pyaltium.magicstrings import MAX_READ_SIZE_BYTES, PCBLIB_HEADER


class PcbLib(AltiumLibraryType):
    """Main object to interact with PCBLib"""

    def _verify_file_type(self, fname: str) -> bool:
        """Check if our magic string is in the header"""
        fh_str = self._read_decode_stream("FileHeader", 128)
        return PCBLIB_HEADER in fh_str

    def _update_header_and_section_keys(self) -> None:
        """Just update class's _header_dict object"""
        fh_str = self._read_decode_stream("FileHeader")
        sk_str = self._read_decode_stream("SectionKeys")

        self._header_dict = altium_string_split(fh_str)
        self._section_keys_list = altium_string_split(sk_str)

    def _update_item_list(self) -> None:
        with olefile.OleFileIO(self._file_name) as ole:
            # Just list storages. We will need to add something to integrate
            # SectionKeys at some point, but the PCBLib flavor of that
            # file makes 0 sense (yet)
            storages_list = ole.listdir(streams=False, storages=True)

            self.items_list = []

            # Need to select only items in storages_list with len 1 (any more
            # would be a subdir) then select 0th element (to get list of str
            # rather than list of list of str)
            for lib_item in (s for s in storages_list if len(s) == 1):
                # Ignore this metadata stream
                if ("fileversioninfo" in lib_item[0].lower()) or (
                    "library" in lib_item[0].lower()
                ):
                    continue

                # We want the paramaters stream within our storage
                lib_item.append("Parameters")

                param_bytestring = ole.openstream(lib_item).read(MAX_READ_SIZE_BYTES)

                # First 4 bytes seem to be random noise
                param_bytestring = param_bytestring[4:]

                # Note: don't really want to ignore errors but
                # '3LED ArrayVertical 2mm TH' has a mystery character
                params_list = altium_string_split(
                    param_bytestring.decode("utf8", errors="ignore")
                )

                footprintref = altium_value_from_key(params_list, "PATTERN")
                description = altium_value_from_key(params_list, "DESCRIPTION")

                height_tmp = altium_value_from_key(params_list, "HEIGHT").lower()

                if "mm" in height_tmp:
                    height = round(float(height_tmp.replace("mm", "")), 2)

                if "mil" in height_tmp:
                    height = round(float(height_tmp.replace("mil", "")) * 0.0254, 2)

                self.items_list.append(
                    PcbLibItem(
                        footprintref=footprintref,
                        description=description,
                        height=height,
                        parent_fname=self._file_name,
                    )
                )


class PcbLibItem(AltiumLibraryItemType):
    def __init__(
        self,
        footprintref: str,
        description: str,
        height: float,
        parent_fname: str,
    ) -> None:
        super().__init__()
        self.footprintref = footprintref
        self.description = description
        self.height = height
        self._file_name = parent_fname

    def _run_load(self) -> None:
        raise NotImplementedError

    def as_dict(self) -> dict:
        """Create a parsable dict."""
        return {
            "footprintref": self.footprintref,
            "description": self.description,
            "height": self.height,
        }
