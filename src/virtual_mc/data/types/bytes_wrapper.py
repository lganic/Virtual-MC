from .generic import Byteable_Object
from ..varint import write_var_int_bytes

# Wrapper class to just make notation easier. 
class Bytes:
    def __init__(self, payload: bytes):
        self.data = payload
    def to_bytes(self):
        return write_var_int_bytes(len(self.data)) + self.data