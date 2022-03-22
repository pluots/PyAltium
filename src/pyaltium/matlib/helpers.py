import re
import uuid
from enum import Enum

HEX_ALPHA_REGEX = re.compile(r"#[0-9A-Fa-f]{8}")


class MatLibTypeID(Enum):
    SOLDERMASK = uuid.UUID("968469a9-c799-46e2-bc61-c05b2553ab48")
