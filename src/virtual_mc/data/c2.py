def convert_to_2s_complement(source_number: int, num_bits: int) -> int:

    if source_number >= 0:
        return source_number

    inverter_num = (2 ** num_bits) - 1

    inverted_bits = inverter_num - abs(source_number)

    return inverted_bits + 1

def convert_from_2s_complement(converted_number: int, num_bits: int):

    check_sign_flag_num = 2 ** (num_bits - 1)

    if converted_number & check_sign_flag_num == 0:
        # Number is positive, no conversion needed
        return converted_number

    inverter_num = (2 ** num_bits) - 1

    inverted_bits = converted_number - 1

    source_number = inverter_num - inverted_bits

    return -source_number # Re-invert number

