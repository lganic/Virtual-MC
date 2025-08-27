import struct
from .generic import Byteable_Object
from ...exceptions import check_range
from ..varint import write_var_int_bytes

class Number(Byteable_Object):

    N: int

    def __init__(self, value):

        check_range(value, 0, (1 << (8 * self.N)) - 1)

        self.value = value

    def to_bytes(self) -> bytes:
        
        # Return the bytes in little endian format

        return self.value.to_bytes(self.N, byteorder='little')    

class Long(Number):
    
    N = 8

class Int(Number):

    N = 4

class VarInt(Byteable_Object, int):
    
    def to_bytes(self) -> bytes:
        
        return write_var_int_bytes(int(self))

class Float(Byteable_Object, float):

    def to_bytes(self) -> bytes:
        return struct.pack('f', float(self))
    
class Double(Byteable_Object, float):

    def to_bytes(self) -> bytes:
        return struct.pack('d', float(self))