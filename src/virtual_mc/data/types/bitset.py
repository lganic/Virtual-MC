from .generic import Byteable_Object
from .numbers import Long
from .array import PrefixedArray

class BitSet(Byteable_Object):

    '''
    Re-implementation of the java bitset class for python
    '''

    def __init__(self, num: int):

        self.bits = [False] * num

    def to_bytes(self):

        output_array = PrefixedArray()

        for i in range(0, len(self.bits), 64):

            chunk = self.bits[i: i + 64]
            long_value = int(chunk[::-1], 2) # Convert reversed chunk into number
            output_array.add_object(Long(long_value))
        
        return output_array.to_bytes()
    
    def set(self, index):

        self.bits[index] = True