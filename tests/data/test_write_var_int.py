import pytest
from virtual_mc.data.varint import write_var_int_bytes, write_var_long_bytes


def test_write_var_int_single_byte():
    # Single-byte VarInt (0 -> 0x00)
    assert write_var_int_bytes(0) == bytes([0x00])

    # Single-byte VarInt (127 -> 0x7F, largest single-byte VarInt)
    assert write_var_int_bytes(127) == bytes([0x7F])

def test_write_var_int_two_bytes():
    # Two-byte VarInt (128 -> 0x80 0x01)
    assert write_var_int_bytes(128) == bytes([0x80, 0x01])

    # Two-byte VarInt (255 -> 0xFF 0x01)
    assert write_var_int_bytes(255) == bytes([0xFF, 0x01])

def test_write_var_int_three_bytes():
    # Three-byte VarInt (16384 -> 0x80 0x80 0x01)
    assert write_var_int_bytes(16384) == bytes([0x80, 0x80, 0x01])

    # Three-byte VarInt (2097151 -> 0xFF 0xFF 0x7F, max 3-byte value)
    assert write_var_int_bytes(2097151) == bytes([0xFF, 0xFF, 0x7F])

def test_write_var_int_four_bytes():
    # Four-byte VarInt (2097152 -> 0x80 0x80 0x80 0x01)
    assert write_var_int_bytes(2097152) == bytes([0x80, 0x80, 0x80, 0x01])

    # Four-byte VarInt (268435455 -> 0xFF 0xFF 0xFF 0x7F, max 4-byte value)
    assert write_var_int_bytes(268435455) == bytes([0xFF, 0xFF, 0xFF, 0x7F])

def test_write_var_int_too_big():
    # Test for VarInt that exceeds 32 bits
    with pytest.raises(TypeError):
        write_var_int_bytes(2**35)

    # Test for VarLong that exceeds 64 bits
    with pytest.raises(TypeError):
        write_var_long_bytes(2**70)

def test_write_var_int_invalid_type():
    # Test for invalid input type
    with pytest.raises(TypeError):
        write_var_int_bytes("not an int")

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
    (-1, bytes([0x81, 0x80, 0x80, 0x80, 0x08]), [129, 128, 128, 128, 8], False),
    (-1073741824, bytes([0x80, 0x80, 0x80, 0x80, 0x0C]), [128, 128, 128, 128, 12], False),
    (-4611686018427387904, bytes([0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0xC0, 0x01]), [128, 128, 128, 128, 128, 128, 128, 128, 192, 1], True),
])
def test_var_int(value, hex_bytes, decimal_bytes, is_long):
    # Test write_var_int


    if is_long:
        assert write_var_long_bytes(value) == hex_bytes
    else:
        assert write_var_int_bytes(value) == hex_bytes