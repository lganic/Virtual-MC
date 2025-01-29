import pytest
from virtual_mc.data.nbt.nbt_util import encode_short

@pytest.mark.parametrize("length_value, short_bytes", [
    (0, bytes([0x00, 0x00])),
    (9, bytes([0x00, 0x09])),
    (11, bytes([0x00, 0x0b])),
    (300, bytes([0x01, 0x2c])),
])
def test_short_encoding(length_value, short_bytes):

    test_bytes = encode_short(length_value)

    assert short_bytes == test_bytes
