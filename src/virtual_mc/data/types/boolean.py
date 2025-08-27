from .generic import Byteable_Object

class Boolean(Byteable_Object):

    def __init__(self, state):

        self.state = state

    def to_bytes(self) -> bytes:

        if self.state:
            return bytes([1])
        
        return bytes([0])