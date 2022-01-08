from pyaltium import PcbLib, SchLib


class TestOpening:
    def test_schlib(self):
        """Make sure we can read items in a schlib."""
        sl = SchLib("tests/files/SchLib1.SchLib")
        assert len(sl.list_items()) > 0

    def test_pcblib(self):
        """Make sure we can read items in a pcblib."""
        pl = PcbLib("tests/files/PcbLib1.PcbLib")
        assert len(pl.list_items()) > 0
