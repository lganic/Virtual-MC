import pytest
from virtual_mc.data.position import convert_position_to_long

def test_position_conversion():

    x = 18357644
    z = -20882616
    y = 831

    converted_position = convert_position_to_long(x, y, z)

    assert converted_position == 0x4607632C15B4833F