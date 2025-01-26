def convert_to_fixed_point(floating_point_num: float, alignment: int) -> int:

    '''
    Convert a floating point number to a fixed point binary integer
    '''

    return int(floating_point_num * (1 << alignment))

def convert_from_fixed_point(fixed_point_num: int, alignment: int) -> float:

    '''
    Convert a fixed point binary integer to a floating point number
    '''

    return fixed_point_num / (1 << alignment)
    