import uuid
from dataclasses import dataclass, field

from pyaltium.helpers import REALNUM, dehumanize, humanize, to_mm
from pyaltium.matlib.base import (
    ColorProperty,
    DielectricBase,
    FinishBase,
    MatLibEntity,
    MatProperty,
)
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


@dataclass
class SolderMask(MatLibEntity):
    type_id: MatLibTypeID = field(default=MatLibTypeID.SOLDERMASK, init=False)
    name: str = ""
    dielectric_constant: REALNUM = 0
    thickness: REALNUM = 0
    manufacturer: str = ""
    frequency: REALNUM = 0
    loss_tangent: REALNUM = 0
    solid: REALNUM = 0
    color: str = "#ffffffff"

    def _get_properties(self) -> list[MatProperty]:
        return [
            MatProperty(
                "Solid",
                "DimValue",
                humanize(self.solid, "%", quantize="0.01", prefix=False),
                {"Dimension": "Relative"},
                atrset="solid",
                setproc=lambda x: float(x.replace("%", "")),
            ),
            ColorProperty(self.color),
            MatProperty(
                "Frequency",
                "DimValue",
                humanize(self.frequency, "Hz", quantize="0.01"),
                {"Dimension": "Frequency"},
                atrset="frequency",
                setproc=lambda x: dehumanize(x, "Hz"),
            ),
            MatProperty(
                "DielectricConstant",
                "DimValue",
                self.dielectric_constant,
                {"Dimension": "Dimensionless"},
                atrset="dielectric_constant",
            ),
            MatProperty(
                "LossTangent",
                "DimValue",
                self.loss_tangent,
                {"Dimension": "Dimensionless"},
                atrset="loss_tangent",
            ),
            MatProperty(
                "Manufacturer", "String", self.manufacturer, atrset="manufacturer"
            ),
            MatProperty("Name", "String", self.name, atrset="name"),
            MatProperty(
                "Thickness",
                "DimValue",
                humanize(self.thickness, "mm", quantize="0.000001", prefix=False),
                {"Dimension": "Length"},
                atrset="thickness",
                setproc=to_mm,
            ),
        ]


_types = (
    Core,
    PrePreg,
    FinishENIG,
    FinishHASL,
    FinishIAu,
    FinishISn,
    FinishOSP,
    SolderMask,
)


def get_type_cls_by_id(type_id):
    """Return the apropriate type class from a type UUID

    :param type_id: Type UUID
    """
    try:
        type_id = MatLibTypeID(type_id)
    except ValueError:
        return None
    return next(filter(lambda t: t.type_id == type_id, _types),None)
