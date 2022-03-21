import uuid
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime


class MatLibProperty:
    name: str
    type: str
    properties: dict = {}
    value: str
    regex = ".*"

    def get_xml(self) -> ET.Element:
        entity = ET.Element("Property")
        entity.set("Type", self.type)
        [entity.set(k, str(v)) for k, v in self.properties.items()]
        entity.text = str(self.value)
        return entity


class ColorMixin:
    name = "Color"
    type = "System.Windows.Media.Color, PresentationCore, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35"
    regex = r"#[0-9A-Fa-f]{8}"


class Solid(MatLibProperty):
    name = "Solid"
    type = "DimValue"
    dimension = "Relative"

    tags = ["Name", "Type", "Dimension"]


class MatLibEntity:
    entity_id: uuid.UUID
    type_id: uuid.UUID
    revision_id: uuid.UUID
    revision_date: datetime
    _properties: list[MatLibProperty]

    def __init__(self) -> None:
        self.entity_id = uuid.uuid4()
        self.revision_id = uuid.uuid4()
        self.revision_date = uuid.uuid4()

    def get_xml(self) -> ET.Element:
        entity = ET.Element("Entity")
        entity.set("Id", str(self.entity_id))
        entity.set("TypeId", str(self.type_id))
        entity.set("RevisionId", str(self.type_id))
        entity.set("RevisionDate", str(self.type_id))
        [entity.append(p.get_xml()) for p in self._properties]
        return entity


class SolderMask(MatLibEntity):
    type_id = uuid.UUID("968469a9-c799-46e2-bc61-c05b2553ab48")


class FinishOSP(MatLibEntity):
    type_id = uuid.UUID("d782f951-a176-457d-bef0-463bd4d45ad7")

    @dataclass
    class _Thickness(MatLibProperty):
        name = "Thickness"
        type = "DimValue"
        properties = {"Dimension": "Length"}
        regex = r"\d+\.?\d*mm"

    @dataclass
    class _Process(MatLibProperty):
        name = "Process"
        type = "String"

    @dataclass
    class _Material(MatLibProperty):
        name = "Material"
        type = "String"

    @dataclass
    class _Material(MatLibProperty, ColorMixin):
        name = "Thickness"
        type = "DimValue"

    def __init__(self) -> None:
        super().__init__()
        self.Thickness = self._Thickness()
        self._properties = [self.Thickness]
