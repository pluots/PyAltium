from pyaltium.sch.helpers import SchPinType, pinstr_worker


def test_byte_arr_str():
    # Default options
    after = "0a0a0a0a0a"
    after_bytes = bytes.fromhex(after)
    s_arr = [
        "0027000001020000000001000000000000",  # preamble
        "0e",  # description size
        str("My Description".encode("utf8").hex()),
        "01",  # formal type
        "07",  # power type
        f"{0b10011:02x}",  # hidden des, 270 rotation
        "3200",  # len 500 (50)
        "6e00",  # x pos 110
        "a6ff",  # y pos -900, (-90).to_bytes(2, "little", signed=True).hex()
        "00000000",  # unknown
        "0b",
        str("Pin () Name".encode("utf8").hex()),
        "06",
        str("PinDes".encode("utf8").hex()),
        "00037c267c",
        after,
    ]

    s_in = bytes.fromhex("".join(s_arr))

    out = {
        "Description": "My Description",
        "PinType": SchPinType.POWER,
        "Rotation": 270,
        "Hide_Designator": False,
        "Hide_Name": True,
        "PinLength": 500,
        "Location.X": 110,
        "Location.Y": -90,
        "Name": "Pin () Name",
        "Designator": "PinDes",
    }

    record, s_out = pinstr_worker(s_in)

    assert record == out
    assert s_out == after_bytes
