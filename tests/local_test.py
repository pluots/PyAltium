import pprint
from pyaltium import SchLib, PcbLib

pp = pprint.PrettyPrinter(indent=4)

# Quick schlib test
sl = SchLib('tests/test_files/Passives.SchLib')
pp.pprint(sl.list_items())

# Quick PCBLib test
pl = PcbLib('tests/test_files/Passives.PcbLib')
pp.pprint(pl.list_items())
