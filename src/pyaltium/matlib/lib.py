import json
import re
import xml.etree.ElementTree as ET
from typing import Iterable, TextIO, TypeVar, Union
from uuid import UUID, uuid4

from pyaltium.matlib.base import MatLibEntity
from pyaltium.matlib.types import get_type_cls_by_id


class MaterialsLibrary:
    """The top level materials library item."""

    # The Altium lib has prototypes for entities only, which holds the matlib items.
    # All others are unused
    types: list
    type_extensions: list
    entities: list[MatLibEntity]
    entity_extensions: list

    serializer_version: str
    library_id: UUID
    version: str
    ns: str

    def __init__(
        self,
        serializer_version="1.1.0.0",
        library_id: Union[str, UUID] = None,
        version: str = "1.1.0.0",
        ns: str = "http://altium.com/ns/Data/ExtensibleLibraries",
    ) -> None:
        self.serializer_version = serializer_version
        if not library_id:
            library_id = uuid4()
        if isinstance(library_id, str):
            library_id = UUID(library_id)
        self.library_id = library_id
        self.version = version
        self.ns = ns  # XML namespaces for maximum annoyance
        self.entities = []

    @classmethod
    def from_et(cls: "MaterialsLibrary", x: ET.Element) -> "MaterialsLibrary":
        """Load in a XML document root as parameters and entities."""
        m = re.match(r"\{(.*)\}", x.tag)
        ns = m.group(1) if m else ""
        instance = cls(
            x.attrib.get("SerializerVersion"),
            x.attrib.get("LibraryId"),
            x.attrib.get("Version"),
            ns,
        )

        for element in x.findall(
            f"./{{{instance.ns}}}Entities/{{{instance.ns}}}Entity"
        ):
            type_id = element.attrib.get("TypeId")
            type_cls = get_type_cls_by_id(type_id)
            if type_cls:
                instance.entities.append(type_cls.from_et(element, ns))

        return instance

    def _get_xml(self) -> ET.ElementTree:
        ns = f"{{{self.ns}:}}" if self.ns else ""
        root = ET.Element(f"{ns}Entity")
        root.set("SerializerVersion", self.serializer_version)
        root.set("LibraryID", str(self.library_id))
        root.set("Version", self.version)
        ET.SubElement(root, "Types")
        ET.SubElement(root, "TypeExtensions")
        entities = ET.SubElement(root, "Entities")
        ET.SubElement(root, "EntityExtensions")
        [entities.append(e._get_xml()) for e in self.entities]

    def getall(
        self, obj_type: Union[MatLibEntity, tuple[MatLibEntity]]
    ) -> Iterable[MatLibEntity]:
        return filter(lambda x: isinstance(x, obj_type), self.entities)

    @classmethod
    def loads(cls, s):
        return cls.from_et(ET.fromstring(s))

    @classmethod
    def load(cls, file: Union[TextIO, str]):
        """Read this library from an XML file.

        :param file: File name as string or pointer as an IO type. Passed directly to
        xml.etree.ElementTree.ElementTree.parse().
        :type file: Union[TextIO, str]
        """
        return cls.from_et(ET.parse(file).getroot())

    def dumps(self) -> str:
        return ET.tostring(self._get_xml(), encoding="UTF-8", xml_declaration=True)

    def dump(self, file: Union[TextIO, str]):
        """Write this library to a file as XML.

        :param file: File name as string or pointer as an IO type. Passed directly to
        xml.etree.ElementTree.ElementTree.write().
        :type file: Union[TextIO, str]
        """
        self._get_xml().write(file, encoding="UTF-8", xml_declaration=True)
