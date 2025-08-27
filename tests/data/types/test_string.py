import pytest
from virtual_mc.data.types import String

def test_string_conversion():

    k = String('Hello World!')

    bt = k.to_bytes()

    assert bt == bytes([0x0C, 0x48, 0x65, 0x6C, 0x6C, 0x6F, 0x20, 0x57, 0x6F, 0x72, 0x6C, 0x64, 0x21])

def test_string_addition():

    k1 = String('Hello')
    k2 = String('Hello')

    k3 = String(k1 + k2) # Not sure if there is a workaround to the String call due to the inheritance

    assert len(k3) == 10