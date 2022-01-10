import matplotlib.pyplot as plt

from pyaltium.base import AltiumLibItemMixin
from pyaltium.sch.libitemrecord import (
    SchLibItemRecord,
    get_sch_lib_item_record,
    handle_pin_records,
)


class SchLibItem(AltiumLibItemMixin[SchLibItemRecord]):
    """A single schematic item in a library.

    :param AltiumLibItemMixin: [description]
    :type AltiumLibItemMixin: [type]
    """

    def __init__(
        self,
        libref: str,
        sectionkey: str,
        description: str,
        partcount: int,
        file_name: str,
        lazyload: bool = False,
    ) -> None:
        super().__init__()
        self.libref = libref
        self.sectionkey = sectionkey
        self.description = description
        self.partcount = partcount
        self.lazyload = lazyload
        self.file_name = file_name

        if not self.lazyload:
            self._load_data()

    def _load_data(self) -> None:
        """Load this item's data to a list of SchLibItem records."""
        # pin_text_data = self._read_decode_stream(
        #     (self.sectionkey, "PinTextData"), decode=False
        # )
        data = self._read_decode_stream((self.sectionkey, "Data"), decode=False)

        # Remove everything before the first "|RECORD"
        while not data.startswith(b"|RECORD"):
            data = data[1:]

        # Split into records
        records = [b"|RECORD" + d for d in data.split(b"|RECORD")[1:]]

        # Split these into their parameters. We need to temporarily escape the
        # |&| that is sometimes used.
        record_params_list: list[dict] = [
            dict(
                split
                for s in rec.replace(b"|&|", b"&&&&").split(b"|")[1:]
                if len(split := s.replace(b"&&&&", b"|&|").split(b"=", 1)) == 2
            )
            for rec in records
        ]

        record_params_list = handle_pin_records(record_params_list)

        self._records = [get_sch_lib_item_record(rp) for rp in record_params_list]

    def draw(self, ax: plt.Axes) -> None:
        """Create the drawing on the axes"""
        part_display_mode = 1
        for record in self.records:
            record.draw(ax=ax, part_display_mode=part_display_mode)

    def as_dict(self) -> dict:
        """Create a parsable dict."""
        return {
            "libref": self.libref,
            "description": self.description,
            "partcount": self.partcount,
            "sectionkey": self.sectionkey,
        }

    def __repr__(self) -> str:
        return f"<SchLibItem> {self.libref}"

    def __str__(self) -> str:
        return self.libref
