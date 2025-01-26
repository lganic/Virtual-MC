import pytest
from virtual_mc.data.c2 import convert_to_2s_complement

def test_tc_positive_value():

    assert convert_to_2s_complement(18357644, 26) == 18357644

def test_tc_negative_value():

    result = 0b10110000010101101101001000 

    value = -20882616

    assert convert_to_2s_complement(value, 26) == result

@pytest.mark.parametrize("bits_in, bits_out", [
    (0, 0),
    (1, 1),
    (2, 2),
    (126, 126),
    (127, 127),
    (-128, 128),
    (-127, 129),
    (-126, 130),
    (-2, 254),
    (-1, 255)
])
def test_tc_8_bit_int(bits_in, bits_out):
    # Test read_var_int
    assert convert_to_2s_complement(bits_in, 8) == bits_out