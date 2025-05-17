from ..data import parsing_utils
from ..data.types.generic import Byteable_Object
from ..data.varint import read_var_int_bytes, get_length_var_int
from .utilities import get_server_protocol_version

# Cache this value, so we don't constantly have to fetch it from disk
SERVER_PROTOCOL_VERSION = get_server_protocol_version()

STATUS = 1
LOGIN = 2
TRANSFER = 3

def parse_handshake(bytes):

    assert bytes[0] == 0
    bytes = bytes[1:]

    protocol_version, bytes = parsing_utils.fetch_and_read_varint(bytes)

    if protocol_version != SERVER_PROTOCOL_VERSION:
        print('WARNING!: Server protocol and client protocol are different!')
    
    server_address, bytes = parsing_utils.parse_string(bytes)

    server_port = int.from_bytes(bytes[:2], byteorder='little')

    bytes = bytes[2:]

    next_state = bytes[0] # This is technically a varint, but the values are never big enough to need more than 1 byte

    if next_state == 0 or next_state > 3:
        raise ValueError(f"Next state is invalid. Current accepted types are: Status(1), Login(2), Transfer(3). Got a value of: {next_state}")

    return protocol_version, server_address, server_port, next_state