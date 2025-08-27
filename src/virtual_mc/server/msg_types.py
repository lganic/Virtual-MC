from enum import Enum

class Msg_Type(Enum):
    HANDSHAKE = 1
    SERVER_PING = 2
    LOGIN = 3
    PING = 4
    ENCRYPTION = 5
    CLIENT_CONFIG = 6
    LOGIN_ACK = 7
    PLUGIN_MSG = 8
    KNOWN_PACKS_MSG = 8