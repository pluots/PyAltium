import matplotlib.patches as patches
import matplotlib.pyplot as plt

from pyaltium.base import (
    AltiumLibraryItemType,
    AltiumLibraryType,
    ObjectRecord,
    SchematicRecord,
)
from pyaltium.helpers import (
    altium_string_split,
    altium_value_from_key,
    eval_bool,
    eval_color,
    re_before_first_record,
    re_split_exclude_ampersand,
    sch_sectionkeys_to_dict,
)
from pyaltium.magicstrings import SCHLIB_HEADER, SchematicRecord, get_sch_record


class SchLib(AltiumLibraryType):
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
                    parent_fname=self._file_name,
                )
            )


class SchLibItem(AltiumLibraryItemType):
    def __init__(
        self,
        libref: str,
        sectionkey: str,
        description: str,
        partcount: int,
        parent_fname: str,
    ) -> None:
        super().__init__()
        self.libref = libref
        self.name = libref
        self.sectionkey = sectionkey
        self.description = description
        self.partcount = partcount
        self._file_name = parent_fname

    def _run_load(self) -> None:
        pin_text_data = self._read_decode_stream(
            (self.sectionkey, "PinTextData"), decode=False
        )
        data = self._read_decode_stream((self.sectionkey, "Data"))

        # Remove everything before the first "|RECORD"
        data = re_before_first_record.sub("|RECORD", data)

        # Split into records
        records = [f"|RECORD{d}" for d in data.split("|RECORD")[1:]]

        # Split these into their parameters
        records = [
            dict(
                s.split("=")
                for s in rec.replace("|&|", "&&&&").split("|")[1:]
                if len(s.split("=")) > 1
            )
            for rec in records
        ]

        # Turn it into a list of objects
        records = [
            ObjectRecord(get_sch_record(rec.get("RECORD", 0)), rec) for rec in records
        ]
        print(records)

        self._loaded_data = records

    def _draw(self, ax: plt.Axes) -> None:
        """Create the drawing on the axes"""
        records = self._loaded_data
        part_display_mode = 1
        for record in records:
            typ = record.record_type
            params = record.parameters
            try:
                display_mode = int(params.get("OwnerPartDisplayMode", 1))
                part_id = params.get("OwnerPartID", 1)

                if display_mode != part_display_mode:
                    continue

                if typ == SchematicRecord.RECTANGLE:
                    bl_x = float(params.get("Location.X", 0))
                    bl_y = float(params.get("Location.Y", 0))
                    tr_x = float(params.get("Corner.X", 0))
                    tr_y = float(params.get("Corner.Y", 0))
                    linewidth = float(params.get("LineWidth", 0.4)) * 10
                    is_solid = eval_bool(params.get("IsSolid", "1"))
                    border_color = eval_color(params.get("Color"))
                    fill_color = eval_color(params.get("AreaColor"))

                    fill_color = fill_color if is_solid else "none"

                    rect = patches.Rectangle(
                        (bl_x, bl_y),
                        width=tr_x - bl_x,
                        height=tr_y - bl_y,
                        linewidth=linewidth,
                        edgecolor=border_color,
                        facecolor=fill_color,
                    )
                    ax.add_patch(rect)

                # elif record.record_type==SchematicRecord.

            except KeyError:
                # If we are missing a key, we wouldn't be able to draw properly
                pass

    def as_dict(self) -> dict:
        """Create a parsable dict."""
        return {
            "libref": self.libref,
            "description": self.description,
            "partcount": self.partcount,
            "sectionkey": self.sectionkey,
        }
