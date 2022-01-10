import olefile

from pyaltium.base import AltiumLibMixin
from pyaltium.helpers import altium_string_split, altium_value_from_key
from pyaltium.magic import MAX_READ_SIZE_BYTES, PCBLIB_HEADER
from pyaltium.pcb.libitem import PcbLibItem


class PcbLib(AltiumLibMixin[PcbLibItem]):
    """Main object to interact with PCBLib"""

    def _verify_file_type(self, fname: str) -> bool:
        """Check if our magic string is in the header"""
        fh_str = self._read_decode_stream("FileHeader", 128)
        return PCBLIB_HEADER in fh_str

    def _update_header_and_section_keys(self) -> None:
        """Just update class's _header_keys_list object"""
        fh_str = self._read_decode_stream("FileHeader")
        sk_str = self._read_decode_stream("SectionKeys")

        self._header_keys_list = altium_string_split(fh_str)
        self._section_keys_list = altium_string_split(sk_str)

    def _update_item_list(self) -> None:
        with olefile.OleFileIO(self.file_name) as ole:
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
                        file_name=self.file_name,
                    )
                )
