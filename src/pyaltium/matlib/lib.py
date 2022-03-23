import re
import xml.etree.ElementTree as ET
from typing import Iterable, TextIO, Union
from uuid import UUID, uuid4

from pyaltium.matlib.base import MatLibEntity
from pyaltium.matlib.types import get_type_cls_by_id

_ns = {"extlib": "http://altium.com/ns/Data/ExtensibleLibraries"}


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

    def _load(self, root: ET.Element):
        """Load in a XML document root as parameters and entities."""
        self.serializer_version = root.attrib.get(
            "SerializerVersion", self.serializer_version
        )
        self.library_id = root.attrib.get("LibraryID", self.library_id)
        self.version = root.attrib.get("Version", self.version)

        m = re.match(r"\{(.*)\}", root.tag)
        self.ns = m.group(1) if m else ""

        for element in root.findall(f"./{{{self.ns}}}Entities/{{{self.ns}}}Entity"):
            type_id = element.attrib.get("TypeId")
            type_cls = get_type_cls_by_id(type_id)
            self.entities.append(type_cls()._load(element))

    def _get_xml(self) -> ET.ElementTree:
        pass

    def getall(
        self, obj_type: Union[MatLibEntity, tuple[MatLibEntity]]
    ) -> Iterable[MatLibEntity]:
        return filter(lambda x: isinstance(x, obj_type), self.entities)

    def loads(self, s):
        self._load(ET.fromstring(s))

    def load(self, file: Union[TextIO, str]):
        """Read this library from an XML file.

        :param file: File name as string or pointer as an IO type. Passed directly to
        xml.etree.ElementTree.ElementTree.parse().
        :type file: Union[TextIO, str]
        """
        self._load(ET.parse(file).getroot())

    def dumps(self) -> str:
        return ET.tostring(self._get_xml(), encoding="UTF-8", xml_declaration=True)

    def dump(self, file: Union[TextIO, str]):
        """Write this library to a file as XML.

        :param file: File name as string or pointer as an IO type. Passed directly to
        xml.etree.ElementTree.ElementTree.write().
        :type file: Union[TextIO, str]
        """
        self._get_xml().write(file, encoding="UTF-8", xml_declaration=True)
