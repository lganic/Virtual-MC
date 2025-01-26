def convert_to_2s_complement(source_number: int, num_bits: int) -> int:

    if source_number >= 0:
        return source_number

    inverter_num = (2 ** num_bits) - 1

    inverted_bits = inverter_num - abs(source_number)

    return inverted_bits + 1