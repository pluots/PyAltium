import pprint

from pyaltium import PcbLib, SchLib

pp = pprint.PrettyPrinter(indent=4)


# Quick schlib test
sl = SchLib("tests/files/sch/SchLib1.SchLib")
# pp.pprint(sl.list_items(as_dict=True))

for item in sl.items_list:
    # if item.name == "Mixed with shape and text":
    #     continue
    print(f"\nProducing {item.name}")
    item.get_svg()


# Quick PCBLib test
pl = PcbLib("tests/files/pcb/PcbLib1.PcbLib")
# pp.pprint(pl.list_items(as_dict=True))
