from pyaltium.helpers import byte_arr_str


def test_byte_arr_str():
    # Default options
    s = b"\x05SSSSSxxxxx"
    assert byte_arr_str(s) == (b"SSSSS", b"xxxxx")

    # Try with longer length info
    s = b"\x05\x00\x00\x00SSSSSxxxxx"
    assert byte_arr_str(s, len_length=4) == (b"SSSSS", b"xxxxx")

    # Try with longer length info
    s = b"\x00\x00\x00\x05SSSSSxxxxx"
    assert byte_arr_str(s, len_length=4, endianness="big") == (b"SSSSS", b"xxxxx")
