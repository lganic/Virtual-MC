from .generic import Byteable_Object

class Boolean(Byteable_Object, bool):

    def to_bytes(self):

        if bool(self):
            return bytes([1])
        
        return bytes([0])