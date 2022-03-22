import re
from decimal import ROUND_HALF_UP, Decimal
from enum import Enum
from uuid import UUID

from pyaltium.helpers import REALNUM

HEX_ALPHA_REGEX = re.compile(r"#[0-9A-Fa-f]{8}")


class MatLibTypeID(Enum):
    """Altium's "magic string" way of identifying library types."""

    SOLDERMASK = UUID("968469a9-c799-46e2-bc61-c05b2553ab48")
    FLEX_COVERLAY = UUID("cd632416-6fe1-4ea1-bb89-01d4b2eae217")
    COPPER_FOIL = UUID("4be0915d-5b0d-4c59-8fae-d57f8650d474")
    FINISH_OSP = UUID("d782f951-a176-457d-bef0-463bd4d45ad7")
    FINISH_ISN = UUID("4dcb0c85-3a3d-4462-9e84-a89dc57f4b84")
    FINISH_IAU = UUID("0800b1d6-17ee-40e9-adba-334c59a1066e")
    FINISH_HASL = UUID("e8b99bb8-b51f-4a6e-a0fc-7439b27f8c76")
    FINISH_ENIG = UUID("b6b5d288-d4b3-4b60-857f-b949da02a37a")
    CORE = UUID("27d70fdc-4c4e-4774-bfac-7efbb48cde47")
    PREPREG = UUID("e04a4e7f-10f0-42df-add7-587710efd89e")
