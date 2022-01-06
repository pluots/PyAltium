"""
types.py

Everything needed to interact with SchLib files
"""


import olefile

from pyaltium.exceptions import PyAltiumError
from pyaltium.helpers import altium_string_split, altium_value_from_key
from pyaltium.magicstrings import MAX_READ_SIZE_BYTES


class AltiumFileType:
    """This class will generally not be exposed.
    Just intended to set up children
    """

    def __init__(self, file_name: str = None) -> None:
        # Initialize variables to be used later
        self._file_name = None
        self._header_dict = {}
        self._section_keys_list = []
        self._items_list = []

        if file_name is not None:
            self.set_file_name(file_name)

    def __respr__(self):
        return self._file_name

    def set_file_name(self, file_name: str) -> None:
        """Check if file is valid (to the best of our ability) then update
        generic information.
        """
        self._file_name = file_name

        if not olefile.isOleFile(file_name):
            raise PyAltiumError("Unable to open file. Is it actually an Altium binary?")

        if not self._verify_file_type(file_name):
            raise PyAltiumError("Appears to be the wrong file type.")

        self._update_header_and_section_keys()
        self._update_item_list()

    def _update_header_and_section_keys(self) -> None:
        """Just update class's _header_dict object."""
        raise NotImplementedError()

    def _update_item_list(self) -> None:
        """Generate a list. This will happen in the inherited class."""
        raise NotImplementedError()

    def _verify_file_type(self, fname: str) -> bool:
        """Verify the file type is what is expected."""
        raise NotImplementedError()

    def _read_decode_stream(
        self, streamname: str, readbytes: int = MAX_READ_SIZE_BYTES
    ) -> str:
        """Read a stream (in one go) and decode it. Maybe add yield in the future."""
        with olefile.OleFileIO(self._file_name) as ole:
            try:
                stream = ole.openstream(streamname)
                return stream.read(readbytes).decode("utf8")
            except OSError:
                # Can't find stream
                return ""
