import re
import uuid
import xml.etree.ElementTree as ET
from ast import Call
from dataclasses import KW_ONLY, dataclass, field
from datetime import datetime
from numbers import Number
from typing import Callable

from pyaltium.helpers import REALNUM
from pyaltium.matlib.helpers import HEX_ALPHA_REGEX, MatLibTypeID


class PropertyValidationError(Exception):
    """Raised when a property does not meet requirements."""

    pass


@dataclass
class MatProperty:
    """Holds information about a Property, a subclass of Entity for materials library."""

    name: str
    type: str
    value: str
    attrib: dict[str, str] = field(default_factory=dict)
    validator: Callable = None
    validator_message: str = ""

    def _get_xml(self):
        """Validate value then return an XML element."""
        if self.validator:
            if not self.__class__.validator(self.value):
                raise PropertyValidationError(self.validator_message)

        prop = ET.Element("Property")
        prop.set("Name", str(self.name))
        prop.set("Type", str(self.type))
        [prop.set(k, v) for k, v in self.attrib.items()]
        prop.text = self.value
        return prop


@dataclass
class ColorProperty(MatProperty):
    """More specific version of a MatProperty, specifically for colors"""

    _: KW_ONLY
    name: str = field(default="Color", init=False)
    type: str = field(
        default="System.Windows.Media.Color, PresentationCore, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35",
        init=False,
    )
    attrib: dict[str, str] = field(default_factory=dict, init=False)
    validator: Call = field(default=lambda x: HEX_ALPHA_REGEX.match(x), init=False)
    validator_message: str = field(
        default="Color needs to be in the format #abababab (hex plus alpha)", init=False
    )


@dataclass
class MatLibEntity:
    """Base class to represent a single item """
    type_id: uuid.UUID = field(init=False)
    entity_id: uuid.UUID = field(default_factory=uuid.uuid4, init=False)
    revision_id: uuid.UUID = field(default_factory=uuid.uuid4, init=False)
    revision_date: datetime = field(default_factory=datetime.utcnow, init=False)

    def _get_properties(self) -> list[MatProperty]:
        """Return a list of properties in XML format.

        :raises NotImplementedError: Method not properly overridden
        :return: List of properties
        :rtype: list[MatProperty]
        """
        raise NotImplementedError

    def _get_xml(self) -> ET.Element:
        entity = ET.Element("Entity")
        entity.set("Id", str(self.entity_id))
        entity.set("TypeId", str(self.type_id))
        entity.set("RevisionId", str(self.type_id))
        entity.set("RevisionDate", f"{self.revision_date.isoformat()}Z")

        [entity.append(p._get_xml()) for p in self._get_properties()]
        return entity


@dataclass
class FinishOSP(MatLibEntity):
    process: str
    material: str
    thickness: REALNUM
    color: str = "#ffffffff"
    type_id: uuid.UUID = field(default=MatLibTypeID.SOLDERMASK, init=False)

    def _get_properties(self):
        return [
            MatProperty(
                "Thickness",
                "DimValue",
                f"{self.thickness}mm",
                {"Dimension": "Length"},
            ),
            MatProperty("Process", "String", self.process),
            MatProperty("Material", "String", self.material),
            ColorProperty(self.color),
        ]


pass
