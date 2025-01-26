SEGMENT_BITS = 0x7F
CONTINUE_BIT = 0x80

SIGNAL_FLAG = 0xFFFFFFFFFFFFFFFFFF80

def read_var_int(data: bytes, is_long=True) -> int:
    """
    Convert var int from bytes to an int
    """

    if not isinstance(data, bytes):
        raise TypeError('Need bytes for conversion')

    if not data:
        raise ValueError('Bytes value is empty!')

    value = 0
    shift = 0  # This represents the bit-shift amount
    for current_byte in data:
        value |= (current_byte & SEGMENT_BITS) << shift

        if (current_byte & CONTINUE_BIT) == 0:
            return value

        shift += 7

        if is_long and shift >= 64:
            raise ValueError('VarLong is too big!')

        elif not is_long and shift >= 32:
            raise ValueError('VarInt is too big!')

    raise ValueError('Incomplete var int data!')  # If we run out of bytes without terminating

def write_var_int(num: int, is_long = True) -> bytes:
    """
    Convert an int to var int bytes
    """

    output_bytes = bytes()

    abs_num = abs(num)

    # Include sign bit as literal portion of number
    if num < 0:
        sign_bit = 0x80000000000000000000 if is_long else 0x8000000000

        abs_num |= sign_bit

    output_bytes_size = 0

    max_size = 10 if is_long else 5

    while True:
        if ((abs_num & SIGNAL_FLAG) == 0):
            output_bytes += bytes([abs_num])

            output_bytes_size += 1

            if output_bytes_size > max_size:
                raise ValueError('Value too big to be represented')

            return output_bytes
        
        output_bytes += bytes([(abs_num & SEGMENT_BITS) | CONTINUE_BIT])

        abs_num >>= 7