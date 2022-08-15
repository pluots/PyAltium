"""base.py

Base matlib types not really meant for direct use outside of source.
"""
from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import KW_ONLY, dataclass, field
from datetime import datetime, timezone
from typing import Callable, Type, TypeVar
from uuid import UUID, uuid4

from dateutil.parser import isoparse

from pyaltium._helpers import (
    REALNUM,
    dehumanize,
    humanize,
    safe_uuid,
    to_celsius,
    to_mm,
)
from pyaltium.matlib._helpers import HEX_ALPHA_REGEX, MatLibTypeID


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
    atrset: str = ""
    setproc: Callable = field(default=lambda x: x)

    def _get_xml(self, ns: str = None):
        """Validate value then return an XML element."""
        if self.validator:
            if not self.__class__.validator(self.value):
                raise PropertyValidationError(self.validator_message)

        prop = ET.Element("Property")
        prop.set("Name", str(self.name))
        prop.set("Type", str(self.type))
        [prop.set(k, str(v)) for k, v in self.attrib.items()]
        prop.text = str(self.value)
        return prop


@dataclass
class ColorProperty(MatProperty):
    """More specific version of a MatProperty, specifically for colors"""

    _: KW_ONLY
    name: str = field(default="Color", init=False)
    type: str = field(
        default="System.Windows.Media.Color, PresentationCore, Version=4.0.0.0,"
        " Culture=neutral, PublicKeyToken=31bf3856ad364e35",
        init=False,
    )
    attrib: dict[str, str] = field(default_factory=dict, init=False)
    validator: Callable = field(default=lambda x: HEX_ALPHA_REGEX.match(x), init=False)
    validator_message: str = field(
        default="Color needs to be in the format #abababab (hex plus alpha)", init=False
    )
    atrset: str = "color"


T = TypeVar("T", bound="MatLibEntity")


@dataclass
class MatLibEntity:
    """Base class to represent a single item. This Entity will contain multiple properties."""

    type_id: str = field(init=False)
    entity_id: UUID = field(default_factory=uuid4, init=False)
    revision_id: UUID = field(default_factory=uuid4, init=False)
    revision_date: datetime = field(default_factory=datetime.utcnow, init=False)
    namespace: str = ""

    @classmethod
    def from_et(cls: Type[T], x: ET.Element, namespace: str = "") -> T:
        """Load in a XML Element to populate class data."""
        instance = cls()
        instance.namespace = namespace
        instance.entity_id = safe_uuid(x.attrib.get("Id"))
        instance.type_id = MatLibTypeID(x.attrib.get("TypeId")).value
        instance.revision_id = safe_uuid(x.attrib.get("RevisionId"))
        instance.revision_date = isoparse(x.attrib.get("RevisionDate"))
        instanceprops = instance._get_properties()

        for xmlprop in x.findall("{*}Property"):
            name = xmlprop.attrib.get("Name")
            prop: MatProperty = next(filter(lambda p: p.name == name, instanceprops))
            if prop:
                val = prop.setproc(xmlprop.text)
                setattr(instance, prop.atrset, val)

        return instance

    def _get_properties(self) -> list[MatProperty]:
        """Return a list of properties in XML format.


        Note for implementation: make sure to reasonably quantize any numbers you perform
        math on, otherwise the XML won't be clean and Altium may have trouble
        importing.

        :raises NotImplementedError: Method not properly overridden
        :return: List of properties
        :rtype: list[MatProperty]
        """
        raise NotImplementedError

    def _get_xml(self) -> ET.Element:
        ns = f"{{{self.namespace}:}}" if self.namespace else ""
        entity = ET.Element(f"{ns}Entity")
        entity.set("Id", str(self.entity_id))
        entity.set("TypeId", str(self.type_id))
        entity.set("RevisionId", str(self.revision_id))
        if self.revision_date.tzinfo is None:
            self.revision_date = self.revision_date.replace(tzinfo=timezone.utc)
        formatted_date = self.revision_date.isoformat().replace("+00:00", "Z")
        entity.set("RevisionDate", f"{formatted_date}")

        [entity.append(p._get_xml()) for p in self._get_properties()]
        return entity
