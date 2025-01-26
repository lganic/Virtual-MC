from typing import Union, TypeAlias
from ..exceptions import check_range
from .c2 import convert_to_2s_complement

Number: TypeAlias = Union[float, int]

def convert_position_to_long(x: Number, y: Number, z:Number) -> int:

    # Round out fields to int
    x = round(x)
    y = round(y)
    z = round(z)

    max_26 = 33554431 # 2^25-1
    min_26 = -33554432 # -2^25

    max_12 = 2047 # 2^11-1
    min_12 = -2048 # 2^11

    # Ensure that x, y, and z are within valid ranges.
    check_range(x, min_26, max_26, name = 'X Coordinate')
    check_range(y, min_12, max_12, name = 'Y Coordinate')
    check_range(z, min_26, max_26, name = 'Z Coordinate')

    # Convert to 2s complement
    x_c = convert_to_2s_complement(x, 26)
    y_c = convert_to_2s_complement(y, 12)
    z_c = convert_to_2s_complement(z, 26)

    # Assemble final long
    return (x_c << 38) + (z_c << 12) + y_c