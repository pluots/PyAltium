from dataclasses import dataclass, field

from pyaltium._helpers import REALNUM, dehumanize, humanize, to_mm
from pyaltium.matlib._helpers import MatLibTypeID
from pyaltium.matlib.base import ColorProperty, MatLibEntity, MatProperty, to_celsius


@dataclass
class DielectricBase(MatLibEntity):
    """Base class used for all dielectrics, with common elements.

    Construction: e.g. 2113 or 1-2113
    Resin: A percent, 0-100
    Glass temp: glass transistion temp in celsius"""

    name: str = ""
    dielectric_constant: REALNUM = 0
    thickness: REALNUM = 0
    glass_trans_temp: REALNUM = 0
    manufacturer: str = ""
    construction: str = ""
    resin_pct: REALNUM = 0
    frequency: REALNUM = 0
    loss_tangent: REALNUM = 0

    def _get_properties(self) -> list[MatProperty]:
        return [
            MatProperty(
                "Constructions", "String", self.construction, atrset="construction"
            ),
            MatProperty(
                "Resin",
                "DimValue",
                humanize(self.resin_pct, "%", quantize="0.01", prefix=False),
                {"Dimension": "Relative"},
                atrset="resin_pct",
                setproc=lambda x: float(x.replace("%", "")),
            ),
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
                "GlassTransTemp",
                "DimValue",
                humanize(
                    self.glass_trans_temp,
                    "C",
                    quantize="0.01",
                    prefix=False,
                ),
                {"Dimension": "Temperature"},
                atrset="glass_trans_temp",
                setproc=to_celsius,
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


@dataclass
class FinishBase(MatLibEntity):
    """Base class used for all finishes, with common elements."""

    process: str = ""
    material: str = ""
    thickness: REALNUM = 0
    color: str = "#ffffffff"

    def _get_properties(self) -> list[MatProperty]:
        return [
            MatProperty(
                "Thickness",
                "DimValue",
                humanize(self.thickness, "mm", quantize="0.000001", prefix=False),
                {"Dimension": "Length"},
                atrset="thickness",
                setproc=to_mm,
            ),
            MatProperty("Process", "String", self.process, atrset="process"),
            MatProperty("Material", "String", self.material, atrset="material"),
            ColorProperty(self.color),
        ]


@dataclass
class Core(DielectricBase):
    """A core"""
    type_id: MatLibTypeID = field(default=MatLibTypeID.CORE.value, init=False)


@dataclass
class PrePreg(DielectricBase):
    type_id: MatLibTypeID = field(default=MatLibTypeID.PREPREG.value, init=False)


@dataclass
class FinishENIG(FinishBase):
    type_id: MatLibTypeID = field(default=MatLibTypeID.FINISH_ENIG.value, init=False)


@dataclass
class FinishHASL(FinishBase):
    type_id: MatLibTypeID = field(default=MatLibTypeID.FINISH_HASL.value, init=False)


@dataclass
class FinishIAu(FinishBase):
    type_id: MatLibTypeID = field(default=MatLibTypeID.FINISH_IAU.value, init=False)


@dataclass
class FinishISn(FinishBase):
    type_id: MatLibTypeID = field(default=MatLibTypeID.FINISH_ISN.value, init=False)


@dataclass
class FinishOSP(FinishBase):
    type_id: MatLibTypeID = field(default=MatLibTypeID.FINISH_OSP.value, init=False)


@dataclass
class SolderMask(MatLibEntity):
    type_id: MatLibTypeID = field(default=MatLibTypeID.SOLDERMASK.value, init=False)
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
    return next(filter(lambda t: t.type_id == type_id, _types), None)
