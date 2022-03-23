import xml.etree.ElementTree as ET
from datetime import datetime
from uuid import UUID
from xml.etree.ElementTree import dump

from pyaltium.matlib.base import MatLibEntity
from pyaltium.matlib.types import (
    Core,
    FinishENIG,
    FinishHASL,
    FinishIAu,
    FinishISn,
    FinishOSP,
    PrePreg,
    SolderMask,
)
from tests.test_matlib.types_xml import TypesXML


def canonicalize_XML(x=None, s: str = None):
    """Canonicalizes XML strings, so they are safe to compare directly.

    Strips white space from text content.

    x is XML Element type, s is a string as an alternative."""

    if s:
        x = ET.fromstring(s)
    xstr = ET.tostring(x)
    return ET.canonicalize(xstr, strip_text=True)


class BaseTypeTest:
    s_match: str

    def validate_xml_match(self, e: MatLibEntity, s: str = None):
        if s is None:
            s = self.s_match
        assert canonicalize_XML(e._get_xml()) == canonicalize_XML(s=s)


class TestCore(BaseTypeTest):
    s_match = TypesXML.CORE

    def test_create(self):
        e = Core(
            name="Core Name",
            dielectric_constant=4.0,
            thickness=0.1,
            glass_trans_temp=180,
            manufacturer="Manufacturer Name",
            construction="1080",
            resin_pct=40,
            frequency=1e9,
            loss_tangent=0.01,
        )
        e.entity_id = UUID(int=0)
        e.revision_id = UUID(int=1)
        e.revision_date = datetime(2022, 2, 2, 16, 40, 30, 765432)

        self.validate_xml_match(e)

    def test_load(self):
        e = Core()
        e._load(ET.fromstring(TypesXML.CORE))
        self.validate_xml_match(e)


class TestPrePreg(BaseTypeTest):
    s_match = TypesXML.PREPREG

    def test_create(self):
        e = PrePreg(
            name="Prepreg Name",
            dielectric_constant=4.0,
            thickness=0.1,
            glass_trans_temp=180,
            manufacturer="Manufacturer Name",
            construction="1x1080",
            resin_pct=40,
            frequency=1e9,
            loss_tangent=0.01,
        )
        e.entity_id = UUID(int=0)
        e.revision_id = UUID(int=1)
        e.revision_date = datetime(2022, 2, 2, 16, 40, 30, 765432)

        self.validate_xml_match(e)

    def test_load(self):
        e = PrePreg()
        e._load(ET.fromstring(TypesXML.PREPREG))
        self.validate_xml_match(e)


class TestENIG(BaseTypeTest):
    s_match = TypesXML.FINISH_ENIG

    def test_create(self):
        e = FinishENIG(
            process="Electroless nickle immersion gold",
            material="Nickel, gold",
            thickness=0.004,
            color="#FFFFFFFF",
        )

        e.entity_id = UUID(int=0)
        e.revision_id = UUID(int=1)
        e.revision_date = datetime(2022, 2, 2, 16, 40, 30, 765432)

        self.validate_xml_match(e)

    def test_load(self):
        e = FinishENIG()
        e._load(ET.fromstring(TypesXML.FINISH_ENIG))
        self.validate_xml_match(e)


class TestSolderMask(BaseTypeTest):
    s_match = TypesXML.SOLDERMASK

    def test_create(self):
        e = SolderMask(
            name="Test Soldermask",
            dielectric_constant=3,
            thickness=0.05,
            manufacturer="Manufacturer",
            frequency=1e9,
            loss_tangent=0.1,
            solid=4,
            color="#008800FF",
        )

        e.entity_id = UUID(int=0)
        e.revision_id = UUID(int=1)
        e.revision_date = datetime(2022, 2, 2, 16, 40, 30, 765432)

        self.validate_xml_match(e)

    def test_load(self):
        e = SolderMask()
        e._load(ET.fromstring(TypesXML.SOLDERMASK))
        self.validate_xml_match(e)
