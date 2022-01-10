"""base.py

Baase classes for everything we do
"""


from typing import AnyStr, Generic, Iterable, List, TypeVar, Union

import matplotlib.pyplot as plt
import olefile

from pyaltium.exceptions import PyAltiumError
from pyaltium.magic import MAX_READ_SIZE_BYTES


class OleMixin:
    """Helper functions for anything with an ole file_name object."""

    def __init__(self) -> None:
        self.file_name = ""

    def _list_storages(self):
        """List all storages (directories) in the olefile"""
        with olefile.OleFileIO(self.file_name) as ole:
            return ole.listdir()

    def _read_decode_stream(
        self,
        streamname: Union[str, Iterable],
        readbytes: int = MAX_READ_SIZE_BYTES,
        decode: Union[str, bool] = "utf8",
    ) -> AnyStr:
        """Read a stream (in one go) and decode it. Maybe add yield in the future."""
        with olefile.OleFileIO(self.file_name) as ole:
            try:
                str_read = ole.openstream(streamname).read(readbytes)
                if decode:
                    return str_read.decode(decode, "ignore").removesuffix("\x00")
                return str_read
            except OSError:
                # Can't find stream
                return "" if decode else b""


class AltiumFileMixin(OleMixin):
    """This class will generally not be exposed.
    Just intended to set up children
    """

    def __init__(self, file_name: str = None, lazyload: bool = False) -> None:
        """Initialize variables to be used later"""
        self.file_name = ""
        self._header_keys_list: List[bytes] = []
        self._section_keys_list: List[bytes] = []
        self.lazyload = lazyload

        if file_name is not None:
            self.setfile_name(file_name)

    def __repr__(self):
        return f"AltiumFileMixin({self.file_name})"

    def setfile_name(self, file_name: str) -> None:
        """Check if file is valid (to the best of our ability) then update
        generic information.
        """
        self.file_name = file_name

        if not olefile.isOleFile(file_name):
            raise PyAltiumError("Unable to open file. Is it actually an Altium binary?")

        if not self._verify_file_type(file_name):
            raise PyAltiumError("Appears to be the wrong file type.")

        self._update_header_and_section_keys()
        self._update_item_list()

    def _update_header_and_section_keys(self) -> None:
        """Just update class's _header_keys_list object."""
        raise NotImplementedError()

    def _update_item_list(self) -> None:
        """Generate a list. This will happen in the inherited class."""
        raise NotImplementedError()

    def _verify_file_type(self, fname: str) -> bool:
        """Verify the file type is what is expected."""
        raise NotImplementedError()


LibItemType = TypeVar("LibItemType")


class AltiumLibMixin(AltiumFileMixin, Generic[LibItemType]):
    """An item in a library.

    Library items should be able to load themselves from a file."""

    def __init__(self, file_name: str = None, lazyload: bool = False) -> None:
        self.items_list: List[LibItemType] = []
        super().__init__(file_name=file_name, lazyload=lazyload)

    def list_items(self, as_dict=True) -> list[LibItemType]:
        """Return a list of all the items.

        Optionally return them as a dictionary."""

        if not as_dict:
            return self.items_list

        return [item.as_dict() for item in self.items_list]


RecordType = TypeVar("RecordType")


class AltiumLibItemMixin(OleMixin, Generic[RecordType]):
    """Single item in a library."""

    def __init__(self) -> None:
        self._records: List[RecordType] = []

    def as_dict(self) -> dict:
        raise NotImplementedError

    def _load_data(self) -> None:
        """Load data from the owner file."""
        raise NotImplementedError

    @property
    def records(self) -> List[RecordType]:
        """Load data if it hasn't been loaded yet. If it has, return it."""
        if self._records is None:
            self._load_data()
        return self._records

    @property
    def name(self) -> str:
        return str(self)

    def draw(self, ax: plt.Axes) -> None:
        """Draw self on a canvas."""
        raise NotImplementedError

    def get_svg(self):
        fig, ax = plt.subplots()
        ax.set_aspect("equal")
        self.draw(ax)
        ax.axis("off")
        ax.autoscale(tight=True)
        fig.savefig(
            f"testout/{self.name}.svg",
            dpi=1200,
            transparant=True,
            bbox_inches="tight",
            pad_inches=0,
        )
        fig.savefig(
            f"testout/{self.name}.png",
            dpi=1200,
            transparant=True,
            bbox_inches="tight",
            pad_inches=0,
        )
