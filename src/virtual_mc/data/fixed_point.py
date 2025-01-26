def convert_to_fixed_point(floating_point_num: float, alignment: int) -> int:

    return int(floating_point_num * (1 << alignment))

def convert_from_fixed_point(fixed_point_num: int, alignment: int) -> float:

    return fixed_point_num / (1 << alignment)
    