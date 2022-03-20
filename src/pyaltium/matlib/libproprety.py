import xml.etree.ElementTree as ET


class MatLibProperty:
    @property
    def xml(self):
        return ET.SubElement


class ColorMixin:
    pass


class Solid(MatLibProperty):
    name = "Solid"
    type = "DimValue"
    dimension = "Relative"

    tags = ["Name", "Type", "Dimension"]
