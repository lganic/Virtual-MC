from .generic import Byteable_Object

# Wrapper class to just make notation easier. 
class Bytes:
    def __init__(self, payload: bytes):
        self.data = payload
    def to_bytes(self):
        return self.data