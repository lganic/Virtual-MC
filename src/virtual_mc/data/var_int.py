SEGMENT_BITS = 0x7F
CONTINUE_BIT = 0x80

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
