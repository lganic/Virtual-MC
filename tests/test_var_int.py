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
