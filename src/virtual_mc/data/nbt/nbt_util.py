def encode_short(n: int):

    return n.to_bytes(2, 'big')

def encode_int(n: int):

    return n.to_bytes(4, 'big')

def decode_short(b: bytes) -> int:

    if len(b) != 2:
        raise ValueError(f"decode_short expects 2 bytes, got {len(b)} bytes.")

    return int.from_bytes(b, 'big')


def decode_int(b: bytes) -> int:

    if len(b) != 4:
        raise ValueError(f"decode_int expects 4 bytes, got {len(b)} bytes.")

    return int.from_bytes(b, 'big')
