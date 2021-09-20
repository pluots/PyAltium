import pprint
from pyaltium import SchLib

sl = SchLib('tests/test_files/Passives.SchLib')
pp = pprint.PrettyPrinter(indent=4)

pp.pprint(sl.list_items())
