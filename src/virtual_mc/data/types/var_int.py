from .generic import Byteable_Object
from ..var_int import write_var_int

class VarInt(Byteable_Object, int):
    
    def to_bytes(self):
        
        return write_var_int(int(self))