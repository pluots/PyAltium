import math
from typing import Iterable, Union

import matplotlib.patches as patches
import matplotlib.pyplot as plt

from pyaltium.helpers import eval_bool, eval_color, getfloat, getint, normalize_dict
from pyaltium.sch.helpers import SchLibItemRecordType, SchPinType, pinstr_to_records


def get_sch_record_type(value: Union[str, int]):
    try:
        return SchLibItemRecordType(int(value))
    except ValueError:
        return SchLibItemRecordType(0)


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

    def __init__(
        self,
        parameters: dict,
    ) -> None:
        self.parameters = normalize_dict(parameters)
        self.record_type = get_sch_record_type(self.parameters.get("RECORD", 0))

        records = handle_pin_records(records)

    def draw(self, ax: plt.Axes, part_display_mode: int = 1) -> None:
        """Draw this single object on matplotlib axes."""
        typ = self.record_type
        params = self.parameters

        try:
            display_mode = int(params.get("OwnerPartDisplayMode", 1))
            part_id = params.get("OwnerPartID", 1)

            if display_mode != part_display_mode:
                return

            loc_x = getint(params, "Location.X")
            loc_y = getint(params, "Location.Y")
            rotation = getint(params, "Rotation")
            linewidth = getfloat(params, "LineWidth", 0.4) * 10
            color = eval_color(params.get("Color"))

            if typ == SchLibItemRecordType.RECTANGLE:
                tr_x = getint(params, "Corner.X")
                tr_y = getint(params, "Corner.Y")
                is_solid = eval_bool(params.get("IsSolid", "1"))
                fill_color = eval_color(params.get("AreaColor"))

                fill_color = fill_color if is_solid else "none"
                print(f"RECT {(loc_x, loc_y)} {(tr_x - loc_x,tr_y - loc_y)}")
                rect = patches.Rectangle(
                    (loc_x, loc_y),
                    width=tr_x - loc_x,
                    height=tr_y - loc_y,
                    linewidth=linewidth,
                    edgecolor=color,
                    facecolor=fill_color,
                )
                ax.add_patch(rect)

            elif typ == SchLibItemRecordType.PIN:
                pinlength = getint(params, "PinLength")
                print(f"PIN {(loc_x, loc_y)} {pinlength}")
                x1 = loc_x + math.cos(math.radians(rotation)) * pinlength
                y1 = loc_y + math.sin(math.radians(rotation)) * pinlength
                ax.plot((loc_x, x1), (loc_y, y1), "k", linewidth=linewidth)

            elif typ == SchLibItemRecordType.LABEL:
                just = getint(params, "Justification", 0)
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
                jm = justMap[just]
                ax.text(
                    loc_x,
                    loc_y,
                    params.get("Text", ""),
                    color=color,
                    verticalalignment=jm[0],
                    horizontalalignment=jm[1],
                )

            # else:
            #     print(typ)

            # elif record.record_type==SchLibItemRecord.

        except KeyError:
            # If we are missing a key, we wouldn't be able to draw properly
            pass

    def __repr__(self) -> str:
        return f"<SchLibItemRecord> {self.record_type.name}"
