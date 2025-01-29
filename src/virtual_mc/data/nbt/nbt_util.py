def encode_short(n: int):

    return n.to_bytes(2, 'big')

def encode_int(n: int):

    return n.to_bytes(4, 'big')