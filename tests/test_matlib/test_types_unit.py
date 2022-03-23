import xml.etree.ElementTree as ET
from datetime import datetime
from uuid import UUID
from xml.etree.ElementTree import dump

from pyaltium.matlib.types import (
    Core,
    FinishENIG,
    FinishHASL,
    FinishIAu,
    FinishISn,
    FinishOSP,
    PrePreg,
)

CORE_XML = """<Entity Id="00000000-0000-0000-0000-000000000000" TypeId="27d70fdc-4c4e-4774-bfac-7efbb48cde47" RevisionId="00000000-0000-0000-0000-000000000001" RevisionDate="2022-02-02T16:40:30.765432Z">
      <Property Name="Constructions" Type="String">1080</Property>
      <Property Name="Resin" Type="DimValue" Dimension="Relative">40%</Property>
      <Property Name="Frequency" Type="DimValue" Dimension="Frequency">1GHz</Property>
      <Property Name="DielectricConstant" Type="DimValue" Dimension="Dimensionless">4.0</Property>
      <Property Name="LossTangent" Type="DimValue" Dimension="Dimensionless">0.01</Property>
      <Property Name="GlassTransTemp" Type="DimValue" Dimension="Temperature">180C</Property>
      <Property Name="Manufacturer" Type="String">Manufacturer Name</Property>
      <Property Name="Name" Type="String">Core Name</Property>
      <Property Name="Thickness" Type="DimValue" Dimension="Length">0.1mm</Property>
    </Entity>"""


def canonicalize_XML(x=None, s: str = None):
    """Canonicalizes XML strings, so they are safe to compare directly.

    Strips white space from text content.

    x is XML Element type, s is a string as an alternative."""

    if s:
        x = ET.fromstring(s)
    xstr = ET.tostring(x)
    return ET.canonicalize(xstr, strip_text=True)


def test_core_create():
    e = Core("Core Name", 4.0, 0.1, 180, "Manufacturer Name", "1080", 40, 1e9, 0.01)
    e.entity_id = UUID(int=0)
    e.revision_id = UUID(int=1)
    e.revision_date = datetime(2022, 2, 2, 16, 40, 30, 765432)

    assert canonicalize_XML(e._get_xml()) == canonicalize_XML(s=CORE_XML)


def test_core_load():
    e = Core()
    e._load(ET.fromstring(CORE_XML))

    assert canonicalize_XML(e._get_xml()) == canonicalize_XML(s=CORE_XML)
