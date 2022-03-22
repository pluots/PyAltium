import uuid
import xml.etree.ElementTree as ET
from typing import TextIO

from pyaltium.matlib.base import MatLibItem


class MaterialsLibrary:
    xml: ET.Element
    entities: list[MatLibItem]

    def __init__(self) -> None:
        # Set xml equal to headers by default
        pass

    def loads(self, s):
        self.xml = ET.fromstring(s)

    def load(self, fpointer: TextIO):
        self.xml = ET.fromstring(fpointer.read())

    def dumps(self) -> str:
        pass

    def dump(self, fpointer):
        pass
