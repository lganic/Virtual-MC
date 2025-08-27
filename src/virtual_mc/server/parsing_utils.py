
import uuid
from typing import Literal, Tuple

from ..data.varint import read_var_int_bytes, get_length_var_int
from . import parsing_utils
from ..data.types import Byteable_Object
from ..data.varint import read_var_int_bytes, get_length_var_int
from .utilities import get_server_protocol_version
from .states import State
from .msg_types import Msg_Type

# Cache this value, so we don't constantly have to fetch it from disk
SERVER_PROTOCOL_VERSION = get_server_protocol_version()

def fetch_and_read_varint(bytes):
    varint_length = get_length_var_int(bytes)

    varint_value = read_var_int_bytes(bytes[:varint_length])

    return varint_value, bytes[varint_length:]

def parse_string(bytes):

    string_length, remaining_bytes = fetch_and_read_varint(bytes)

    if string_length > len(remaining_bytes):
        print("WARNING: A number of bytes were just read from the buffer, that were larger than the buffer itself!!!")

    string_value = remaining_bytes[:string_length]

    return string_value, remaining_bytes[string_length:]

def parse_uuid(message):
    if len(message) != 16:
        raise ValueError("Must be exactly 16 bytes for a UUID")
    return uuid.UUID(bytes=message)

def parse_handshake(bytes):
    '''
    Return the protocol version, server address, server port, and next state
    '''

    bytes = bytes[1:]

    protocol_version, bytes = parsing_utils.fetch_and_read_varint(bytes)

    if protocol_version != SERVER_PROTOCOL_VERSION:
        print('WARNING!: Server protocol and client protocol are different!')
    
    server_address, bytes = parsing_utils.parse_string(bytes)

    server_port = int.from_bytes(bytes[:2], byteorder='little')

    bytes = bytes[2:]

    assert len(bytes) == 1

    next_state = bytes[0] # This is technically a varint, but the values are never big enough to need more than 1 byte

    if next_state == 0 or next_state > 3:
        raise ValueError(f"Next state is invalid. Current accepted types are: Status(1), Login(2), Transfer(3). Got a value of: {next_state}")

    next_state = {
        1: State.STATUS,
        2: State.LOGIN,
        3: State.TRANSFER
    }[next_state]

    return protocol_version, server_address, server_port, next_state

def parse_00_packet(packet: bytes, state: State) -> Tuple[Literal[1, 2, 3], Tuple]:

    assert packet[0] == 0

    if state is None:
        state = State.STATUS

    if not isinstance(state, State):
        raise ValueError("A non-state was passed to the parsing function")

    if state == State.STATUS:
        if len(packet) == 1:
            # Ping request packet. 
            return Msg_Type.SERVER_PING, ()
        
        return Msg_Type.HANDSHAKE, parse_handshake(packet)

    if state == State.LOGIN:
        username, packet = parse_string(packet[1:])

        uuid = parse_uuid(packet)

        return Msg_Type.LOGIN, (username, uuid)

    if state == State.CONFIGURATION:
        locale, packet = parse_string(packet[1:])
        view_distance = packet[0]
        chat_mode = packet[1]
        colors_enabled = packet[2] == 1
        displayed_parts = packet[3]
        main_hand = packet[4]
        text_filtering = packet[5] == 1
        allow_server_listing = packet[6] == 1
        particle_status = packet[7] == 1

        return Msg_Type.CLIENT_CONFIG, (locale, view_distance, chat_mode, colors_enabled, displayed_parts, main_hand, text_filtering, allow_server_listing, particle_status)

    # TODO: Check for a client info packet, or a teleport request. 

    raise NotImplementedError("I have no idea what to do with this packet.")

def parse_01_packet(packet: bytes, state: State):

    assert packet[0] == 1

    if not isinstance(state, State):
        raise ValueError("A non-state was passed to the parsing function")

    if state is None:
        state = State.STATUS

    if state == State.STATUS:
        return Msg_Type.PING, (packet,)
    
    if state == State.LOGIN:
        shared_secret, packet = parse_string(packet[1:])
        verify_token, _ = parse_string(packet)

        return Msg_Type.ENCRYPTION, (shared_secret, verify_token)
    
    raise NotImplementedError("I have no idea what to do with this packet.")

def parse_02_packet(packet: bytes, state: int):

    if state == State.CONFIGURATION:
        # Serverbound Plugin Message

        # Parses two strings, first is the identifier, then the data. 

        identifier, packet = parse_string(packet[1:])
        data, _ = parse_string(packet)

        return Msg_Type.PLUGIN_MSG, (identifier, packet)
    
    raise NotImplementedError("I have no idea what to do with this packet.")
