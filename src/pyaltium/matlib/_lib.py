from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from typing import Iterable, TextIO, Union
from uuid import UUID, uuid4

from pyaltium.matlib.base import MatLibEntity
from pyaltium.matlib.types import get_type_cls_by_id


class MaterialsLibrary:
    """The top level materials library item.

    This class represents an Altium materials library, which is generally
    """

    # The Altium lib has prototypes for entities only, which holds the matlib items.
    # All others are unused
    types: list
    type_extensions: list
    entities: list[MatLibEntity]
    entity_extensions: list

    serializer_version: str
    library_id: UUID
    version: str
    namespace: str

    def __init__(
        self,
        library_id: Union[str, UUID] = None,
        serializer_version: str = "1.1.0.0",
        version: str = "1.1.0.0",
        namespace: str = "http://altium.com/ns/Data/ExtensibleLibraries",
    ) -> None:
        """Create a new Altium materials library.

        :param library_id: The library ID to set for this version, defaults to
            None
        :type library_id: Union[str, UUID], optional
        :param serializer_version: The Altium materials library version.
            Currently only the default is supported. Defaults to "1.1.0.0"
        :type serializer_version: str, optional
        :param version: Version of the Altium materials library, defaults to
            "1.1.0.0"
        :type version: str, optional
        :param namespace: Namespace of the xml file, defaults to
            "http://altium.com/ns/Data/ExtensibleLibraries"
        :type namespace: _type_, optional
        """
        self.serializer_version = serializer_version
        if not library_id:
            library_id = uuid4()
        if isinstance(library_id, str):
            library_id = UUID(library_id)
        self.library_id = library_id
        self.version = version
        self.namespace = namespace  # XML namespaces for maximum annoyance
        self.entities = []

    @classmethod
    def from_et(cls: "MaterialsLibrary", et: ET.Element) -> "MaterialsLibrary":
        """Load in a XML document root as parameters and entities.
        """
        m = re.match(r"\{(.*)\}", et.tag)
        ns = m.group(1) if m else ""
        instance:MaterialsLibrary = cls(
            et.attrib.get("LibraryId"),
            et.attrib.get("SerializerVersion"),
            et.attrib.get("Version"),
            ns,
        )

        for element in et.findall(
            f"./{{{instance.namespace}}}Entities/{{{instance.namespace}}}Entity"
        ):
            type_id = element.attrib.get("TypeId")
            type_cls = get_type_cls_by_id(type_id)
            if type_cls:
                instance.entities.append(type_cls.from_et(element, ns))

        return instance

    def _get_xml(self) -> ET.ElementTree:
        ns = f"{{{self.namespace}:}}" if self.namespace else ""
        root = ET.Element(f"{ns}ExtensibleLibrary")
        root.set("SerializerVersion", self.serializer_version)
        root.set("LibraryID", str(self.library_id))
        root.set("Version", self.version)
        ET.SubElement(root, "Types")
        ET.SubElement(root, "TypeExtensions")
        entities = ET.SubElement(root, "Entities")
        ET.SubElement(root, "EntityExtensions")
        [entities.append(e._get_xml()) for e in self.entities]

        ET.indent(root)
        return root

    def getall(
        self, obj_type: Union[MatLibEntity, tuple[MatLibEntity]]
    ) -> Iterable[MatLibEntity]:
        """Locate all"""
        return filter(lambda x: isinstance(x, obj_type), self.entities)

    @classmethod
    def loads(cls, s):
        """Read in the material library from an XML string.
        """
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
        """Write this material library to an XML string."""
        return ET.tostring(self._get_xml(), encoding="UTF-8", xml_declaration=True)

    def dump(self, file: Union[TextIO, str]):
        """Write this library to a file as XML.

        :param file: File name as string or pointer as an IO type. Passed directly to
        xml.etree.ElementTree.ElementTree.write().
        :type file: Union[TextIO, str]
        """
        tree = ET.ElementTree(self._get_xml())
        tree.write(file, encoding="UTF-8", xml_declaration=True)
