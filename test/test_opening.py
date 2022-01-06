import pprint

from pyaltium import PcbLib, SchLib

pp = pprint.PrettyPrinter(indent=4)

import pdb

# pdb.set_trace()


class TestOpening:
    def test_schlib(self):
        # Quick schlib test
        sl = SchLib("test/files/SchLib1.SchLib")
        assert len(sl.list_items()) > 0

    def test_pcblib(self):
        # Quick PCBLib test
        pl = PcbLib("test/files/PcbLib1.PcbLib")
        assert len(pl.list_items()) > 0
