import math
from typing import Dict, Iterable, List, TypeVar

import matplotlib.patches as patches
import matplotlib.pyplot as plt

from pyaltium.helpers import eval_bool, eval_color, normalize_dict
from pyaltium.sch.helpers import SchLibItemRecordType, pinstr_to_records


def handle_pin_records(records: Iterable[dict]) -> list:
    """Run through a list of records for a schematic component and handle pins.

    Pins are a bit weird. There is no record type for them so they are just binary
    strings in the middle of other textual records.

    That means we need to go through all the records and explicitely split this off,
    since they just tag along with whatever record preceeded them.
    """

    retlist = []

    for rec in records:
        newrecords = []
        for key, val in rec.items():
            # If there is nothing bytes in the string, we are set
            if b"\x00" not in val:
                continue

            # Otherwise, do cleanup
            newval, pinstr = val.split(b"\x00", 1)
            rec[key] = newval

            # If it's too short to be a pin, it's probably just junk so ignore
            if len(pinstr) > 20:
                complete_str = b"\x00" + pinstr
                newrecords.extend(pinstr_to_records(complete_str))

        retlist.append(rec)
        retlist.extend(newrecords)

    return retlist


class SchLibItemRecord:
    """An object record stored in a schematic."""

    rtype: SchLibItemRecordType

    def __init__(
        self,
        parameters: dict,
    ) -> None:
        self.param_dict = normalize_dict(parameters)
        self._load_basic_types()
        self._load()

    def _load_basic_types(self) -> None:
        self.loc_x = self.param_dict.get("Location.X", 0)
        self.loc_y = self.param_dict.get("Location.Y", 0)
        self.rotation = self.param_dict.get("Rotation", 0)
        self.linewidth = self.param_dict.get("LineWidth", 0.4) * 10
        self.color = eval_color(self.param_dict.get("Color", 0x000000))
        self.display_mode = int(self.param_dict.get("OwnerPartDisplayMode", 1))
        self.part_id = self.param_dict.get("OwnerPartID", 1)

    def _load(self) -> None:
        raise NotImplementedError

    def _draw(self, ax: plt.Axes) -> None:
        raise NotImplementedError

    def draw(self, ax: plt.Axes, part_display_mode: int = 1) -> None:
        """Draw this single object on matplotlib axes."""
        if self.display_mode != part_display_mode:
            return

        return self._draw(ax)

    def __repr__(self) -> str:
        return f"<{type(self).__name__} ({self.loc_x},{self.loc_y})"


class SLIRUndefined(SchLibItemRecord):
    rtype = SchLibItemRecordType.UNDEFINED

    def _load(self) -> None:
        pass

    def _draw(self, ax: plt.Axes) -> None:
        pass


class SLIRRectange(SchLibItemRecord):
    rtype = SchLibItemRecordType.RECTANGLE

    def _load(self) -> None:
        self.tr_x = self.param_dict.get("Corner.X", 0)
        self.tr_y = self.param_dict.get("Corner.Y", 0)
        self.is_solid = eval_bool(self.param_dict.get("IsSolid", "1"))
        self.fill_color = eval_color(self.param_dict.get("AreaColor"))

    def _draw(self, ax: plt.Axes) -> None:

        fill_color = self.fill_color if self.is_solid else "none"
        print(
            f"RECT {(self.loc_x, self.loc_y)} "
            f"{(self.tr_x - self.loc_x,self.tr_y - self.loc_y)}"
        )
        rect = patches.Rectangle(
            (self.loc_x, self.loc_y),
            width=self.tr_x - self.loc_x,
            height=self.tr_y - self.loc_y,
            linewidth=self.linewidth,
            edgecolor=self.color,
            facecolor=fill_color,
        )
        ax.add_patch(rect)


class SLIRPin(SchLibItemRecord):
    rtype = SchLibItemRecordType.PIN

    def _load(self) -> None:
        self.pinlength = self.param_dict.get("PinLength", 0)

    def _draw(self, ax: plt.Axes) -> None:
        print(f"PIN {(self.loc_x, self.loc_y)} {self.pinlength}")
        x1 = self.loc_x + math.cos(math.radians(self.rotation)) * self.pinlength
        y1 = self.loc_y + math.sin(math.radians(self.rotation)) * self.pinlength
        ax.plot((self.loc_x, x1), (self.loc_y, y1), "k", linewidth=self.linewidth)


class SLIRLabel(SchLibItemRecord):
    rtype = SchLibItemRecordType.LABEL

    def _load(self) -> None:
        self.pinlength = self.param_dict.get("PinLength", 0)
        just = self.param_dict.get("Justification", 0)
        self.text = self.param_dict.get("Text", "")
        justMap = {
            0: ("bottom", "left"),
            1: ("bottom", "center"),
            2: ("bottom", "right"),
            3: ("center", "left"),
            4: ("center", "center"),
            5: ("center", "right"),
            6: ("top", "left"),
            7: ("top", "center"),
            8: ("top", "right"),
        }
        self.just = justMap[just]

    def _draw(self, ax: plt.Axes) -> None:
        ax.text(
            self.loc_x,
            self.loc_y,
            self.text,
            color=self.color,
            verticalalignment=self.just[0],
            horizontalalignment=self.just[1],
        )


SLIRType = TypeVar("SLIRType", bound=SchLibItemRecord)
_record_type_list: List[SLIRType] = [SLIRUndefined, SLIRRectange, SLIRPin, SLIRLabel]
record_types: Dict[SchLibItemRecordType, SchLibItemRecord] = {
    rcls.rtype: rcls for rcls in _record_type_list
}


def get_sch_lib_item_record(record_params) -> SchLibItemRecord:
    """Returns an instantiated SchLibItemRecord of the apropriate type."""
    type_val = record_params.get("RECORD", 0)
    try:
        rtype = SchLibItemRecordType(int(type_val))
    except ValueError:
        rtype = SchLibItemRecordType(0)

    return record_types[rtype](record_params)
