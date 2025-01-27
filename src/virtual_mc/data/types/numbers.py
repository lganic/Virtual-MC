from .generic import Byteable_Object
from ...exceptions import check_range

class Number(Byteable_Object):

    N: int

    def __init__(self, value):

        check_range(value, 0, (1 << (8 * self.N)) - 1)

        self.value = value

    def to_bytes(self):
        
        # Return the bytes in little endian format

        return self.value.to_bytes(self.N, byteorder='little')    

class Long(Number):
    
    N = 8

class Int(Number):

    N = 4
