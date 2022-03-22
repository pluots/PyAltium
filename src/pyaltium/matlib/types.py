import uuid
from dataclasses import dataclass, field

from pyaltium.helpers import REALNUM
from pyaltium.matlib.base import DielectricBase, FinishBase, MatLibEntity
from pyaltium.matlib.helpers import MatLibTypeID


@dataclass
class Core(DielectricBase):
    type_id: MatLibTypeID = field(default=MatLibTypeID.CORE, init=False)


@dataclass
class PrePreg(DielectricBase):
    type_id: MatLibTypeID = field(default=MatLibTypeID.PREPREG, init=False)


@dataclass
class FinishENIG(FinishBase):
    type_id: MatLibTypeID = field(default=MatLibTypeID.FINISH_ENIG, init=False)


@dataclass
class FinishHASL(FinishBase):
    type_id: MatLibTypeID = field(default=MatLibTypeID.FINISH_HASL, init=False)


@dataclass
class FinishIAu(FinishBase):
    type_id: MatLibTypeID = field(default=MatLibTypeID.FINISH_IAU, init=False)


@dataclass
class FinishISn(FinishBase):
    type_id: MatLibTypeID = field(default=MatLibTypeID.FINISH_ISN, init=False)


@dataclass
class FinishOSP(FinishBase):
    type_id: MatLibTypeID = field(default=MatLibTypeID.FINISH_OSP, init=False)
