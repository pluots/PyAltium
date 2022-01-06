"""
types.py

Everything needed to interact with SchLib files
"""


from typing import Iterable, Union

import matplotlib.pyplot as plt
import olefile

from pyaltium.exceptions import PyAltiumError
from pyaltium.helpers import read_decode_stream
from pyaltium.magicstrings import MAX_READ_SIZE_BYTES, SchematicRecord


class OleMixin:
    """Helper functions for anything with an ole _file_name object."""

    def _list_storages(self):
        with olefile.OleFileIO(self._file_name) as ole:
            return ole.listdir()

    def _read_decode_stream(
        self,
        streamname: Union[str, Iterable],
        readbytes: int = MAX_READ_SIZE_BYTES,
        decode: str = "utf8",
    ) -> str:
        """Read a stream (in one go) and decode it. Maybe add yield in the future."""
        with olefile.OleFileIO(self._file_name) as ole:
            try:
                str_read = ole.openstream(streamname).read(readbytes)
                if decode:
                    return str_read.decode(decode, "ignore").removesuffix("\x00")
                return str_read
            except OSError:
                # Can't find stream
                return "" if decode else b""


class AltiumFileType(OleMixin):
    """This class will generally not be exposed.
    Just intended to set up children
    """

    def __init__(self, file_name: str = None) -> None:
        # Initialize variables to be used later
        self._file_name = None
        self._header_dict = {}
        self._section_keys_list = []
        self.items_list = []

        if file_name is not None:
            self.set_file_name(file_name)

    def __repr__(self):
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


class AltiumLibraryType(AltiumFileType):
    def list_items(self, as_dict=True) -> list:
        """Return a list of all the items.

        Optionally return them as a dictionary."""

        if not as_dict:
            return self.items_list

        return [item.as_dict() for item in self.items_list]


class AltiumLibraryItemType(OleMixin):
    def __init__(self) -> None:
        self._loaded_data = None
        self.name = None

    def _as_dict(self) -> dict:
        raise NotImplementedError

    def _run_load(self) -> None:
        """Set self._storage as needed."""
        raise NotImplementedError

    def _load(self) -> None:
        """Load data from the owner file."""
        if self._loaded_data is not None:
            return
        self._run_load()

    def _draw(self, ax: plt.Axes) -> None:
        raise NotImplementedError

    def get_svg(self):
        self._load()
        fig, ax = plt.subplots()
        self._draw(ax)
        ax.axis("off")
        ax.autoscale(tight=True)
        plt.show()
        fig.savefig(f"testout/{self.name}", bbox_inches="tight", pad_inches=0)


def handle_allpins_obj(s: str):
    count = int(s[0])
    s = s[1:]
    pins = s.split("&&&&")
    pass
    print("h")
    # bytes(pins[0], encoding="raw_unicode_escape").hex()
    # hx=[bytes(p, encoding="raw_unicode_escape").hex(' ',4) for p in pins]


class ObjectRecord:
    """An object record stored in a schematic."""

    def __init__(self, record_type: SchematicRecord, parameters: dict) -> None:
        self.record_type = record_type
        self.parameters = parameters

        pins = self.parameters.get("AllPinCount")
        if pins:
            handle_allpins_obj(pins)

    def __repr__(self) -> str:
        return f"<ObjectRecord> {self.record_type.name}"
