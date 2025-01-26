import pytest
from virtual_mc.data.var_int import read_var_int

def test_read_var_int_single_byte():
    # Single-byte VarInt (0x00 -> 0)
    data = bytes([0x00])
    assert read_var_int(data, is_long=False) == 0

    # Single-byte VarInt (0x7F -> 127, largest single-byte VarInt)
    data = bytes([0x7F])
    assert read_var_int(data, is_long=False) == 127

def test_read_var_int_two_bytes():
    # Two-byte VarInt (0x80 0x01 -> 128)
    data = bytes([0x80, 0x01])
    assert read_var_int(data, is_long=False) == 128

    # Two-byte VarInt (0xFF 0x01 -> 255)
    data = bytes([0xFF, 0x01])
    assert read_var_int(data, is_long=False) == 255

def test_read_var_int_three_bytes():
    # Three-byte VarInt (0x80 0x80 0x01 -> 16384)
    data = bytes([0x80, 0x80, 0x01])
    assert read_var_int(data, is_long=False) == 16384

    # Three-byte VarInt (0xFF 0xFF 0x7F -> 2097151, max 3-byte value)
    data = bytes([0xFF, 0xFF, 0x7F])
    assert read_var_int(data, is_long=False) == 2097151

def test_read_var_int_four_bytes():
    # Four-byte VarInt (0x80 0x80 0x80 0x01 -> 2097152)
    data = bytes([0x80, 0x80, 0x80, 0x01])
    assert read_var_int(data, is_long=False) == 2097152

    # Four-byte VarInt (0xFF 0xFF 0xFF 0x7F -> 268435455, max 4-byte value)
    data = bytes([0xFF, 0xFF, 0xFF, 0x7F])
    assert read_var_int(data, is_long=False) == 268435455

def test_read_var_int_max_valid():
    # Five-byte VarInt (0xFF 0xFF 0xFF 0xFF 0x07 -> 2^31 - 1)
    data = bytes([0xFF, 0xFF, 0xFF, 0xFF, 0x07])
    assert read_var_int(data, is_long=False) == 2**31 - 1

def test_read_var_long_valid():
    # VarLong (0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0x7F -> 2^63 - 1)
    data = bytes([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x7F])
    assert read_var_int(data, is_long=True) == 2**63 - 1

def test_read_var_int_empty_bytes():
    # Test for empty bytes input
    with pytest.raises(ValueError):
        read_var_int(b"")

def test_read_var_int_invalid_type():
    # Test for invalid input type
    with pytest.raises(TypeError):
        read_var_int("not bytes")

def test_read_var_int_too_big():
    # Test for VarInt that exceeds 32 bits
    data = bytes([0xFF] * 5)
    with pytest.raises(ValueError):
        read_var_int(data, is_long=False)

@pytest.mark.parametrize("value, hex_bytes, decimal_bytes, is_long", [
    (0, bytes([0x00]), [0], False),
    (1, bytes([0x01]), [1], False),
    (2, bytes([0x02]), [2], False),
    (127, bytes([0x7F]), [127], False),
    (128, bytes([0x80, 0x01]), [128, 1], False),
    (255, bytes([0xFF, 0x01]), [255, 1], False),
    (25565, bytes([0xDD, 0xC7, 0x01]), [221, 199, 1], False),
    (2097151, bytes([0xFF, 0xFF, 0x7F]), [255, 255, 127], False),
    (2147483647, bytes([0xFF, 0xFF, 0xFF, 0xFF, 0x07]), [255, 255, 255, 255, 7], False),
    (-1, bytes([0xFF, 0x0F]), [255, 15], False),
    (-2147483648, bytes([0x80, 0x80, 0x80, 0x80, 0x08]), [128, 128, 128, 128, 8], False),
])
def test_var_int(value, hex_bytes, decimal_bytes, is_long):
    # Test read_var_int
    assert read_var_int(hex_bytes, is_long=is_long) == value
