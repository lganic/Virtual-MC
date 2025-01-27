import pytest
from virtual_mc.data.types.bitset import BitSet

# Helper function to create a bitset
def create_bitset(bitstring):

    size = len(bitstring)

    s = BitSet(size)

    s.set_states(bitstring)

    return s

# Test cases
def test_to_long_array_single_long():
    # Example: 10 bits fit within one long
    bitset = create_bitset("1010110010")  # 10 bits
    result = bitset.to_long_array()
    # Expected: [0b1010110010] -> In decimal, it's [690]
    assert result == [309]

def test_to_long_array_multiple_longs():
    # Example: 65 bits split into two longs
    bitset = create_bitset("1" * 65)  # 65 bits, all 1
    result = bitset.to_long_array()
    # Expected:
    # First long: 64 ones -> 0xFFFFFFFFFFFFFFFF
    # Second long: 1 one, padded with zeros -> 0x1
    assert result == [0xFFFFFFFFFFFFFFFF, 0x1]

def test_to_long_array_partial_last_long():
    # Example: 70 bits (64 + 6)
    bitset = create_bitset("1" * 70)  # 70 bits, all 1
    result = bitset.to_long_array()
    # Expected:
    # First long: 64 ones -> 0xFFFFFFFFFFFFFFFF
    # Second long: 6 ones, padded with zeros -> 0x3F
    assert result == [0xFFFFFFFFFFFFFFFF, 0x3F]

def test_to_long_array_empty():
    # Example: Empty bitset
    bitset = create_bitset("")  # 0 bits
    result = bitset.to_long_array()
    # Expected: No longs, empty array
    assert result == []

def test_to_long_array_mixed_bits():
    # Example: 130 bits with a mix of 1s and 0s
    bitset = create_bitset("10101010" * 16 + "11110000" * 2)  # 130 bits
    result = bitset.to_long_array()
    assert result == [0x5555555555555555, 0x5555555555555555, 0xF0F]

# # Convert to Bytes tests
# def test_to_bytes_single_long():
#     # Example: 10 bits fit within one long
#     bitset = create_bitset("1010110010")  # 10 bits
#     result = bitset.to_bytes()
#     # Expected: [0b1010110010] -> In decimal, it's [690]
#     assert result == [1, 0, 0, 0, 309]

# def test_to_bytes_multiple_longs():
#     # Example: 65 bits split into two longs
#     bitset = create_bitset("1" * 65)  # 65 bits, all 1
#     result = bitset.to_long_array()
#     # Expected:
#     # First long: 64 ones -> 0xFFFFFFFFFFFFFFFF
#     # Second long: 1 one, padded with zeros -> 0x1
#     assert result == [0xFFFFFFFFFFFFFFFF, 0x1]

# def test_to_bytes_partial_last_long():
#     # Example: 70 bits (64 + 6)
#     bitset = create_bitset("1" * 70)  # 70 bits, all 1
#     result = bitset.to_long_array()
#     # Expected:
#     # First long: 64 ones -> 0xFFFFFFFFFFFFFFFF
#     # Second long: 6 ones, padded with zeros -> 0x3F
#     assert result == [0xFFFFFFFFFFFFFFFF, 0x3F]

# def test_to_bytes_empty():
#     # Example: Empty bitset
#     bitset = create_bitset("")  # 0 bits
#     result = bitset.to_long_array()
#     # Expected: No longs, empty array
#     assert result == []

# def test_to_bytes_mixed_bits():
#     # Example: 130 bits with a mix of 1s and 0s
#     bitset = create_bitset("10101010" * 16 + "11110000" * 2)  # 130 bits
#     result = bitset.to_long_array()
#     assert result == [0x5555555555555555, 0x5555555555555555, 0xF0F]
