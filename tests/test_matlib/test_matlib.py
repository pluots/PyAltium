from pyaltium import MaterialsLibrary


def test_init():
    with open("tests/files/matlib.xml", "r") as f:
        ml = MaterialsLibrary.load(f)

    ml._get_xml()
