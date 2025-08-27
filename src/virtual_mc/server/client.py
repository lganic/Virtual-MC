# Unpacks, and tracks values being sent from the client. 
# Also determines proper responses to certain types of packets (ie. handshakes)

from typing import Union

class Client:
    def __init__(self):
    
        self.prot_version = None
        self.address = None
        self.port = None
        self.current_handshake_state = None

        self.username = None
        self.user_uuid = None

        self.locale = None
        self.view_distance = None