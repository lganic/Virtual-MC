
from .varint import read_var_int_bytes, get_length_var_int

def fetch_and_read_varint(bytes):
    varint_length = get_length_var_int(bytes)

    varint_value = read_var_int_bytes(bytes[:varint_length])

    return varint_value, bytes[varint_length:]

def parse_string(bytes):

    string_length, remaining_bytes = fetch_and_read_varint(bytes)

    string_value = remaining_bytes[:string_length]

    return string_value, remaining_bytes[string_length:]