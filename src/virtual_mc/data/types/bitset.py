from .generic import Byteable_Object
from .numbers import Long
from .array import PrefixedArray

class BitSet(Byteable_Object):

    '''
    Re-implementation of the java bitset class for python
    '''

    def __init__(self, num: int):

        self.bits = [False] * num

    def to_long_array(self):

        output_array = []

        for i in range(0, len(self.bits), 64):

            chunk = self.bits[i: i + 64]
            long_value = int(chunk[::-1], 2) # Convert reversed chunk into number

            output_array.append(long_value)
        
        return output_array

    def to_bytes(self):

        output_array = PrefixedArray()

        for long_value in self.to_long_array():

            output_array.add_object(Long(long_value))
        
        return output_array.to_bytes()
    
    def set(self, index):

        self.bits[index] = True

    def set_states(self, states: str):

        '''
        Takes in a string of 0 and 1, i.e : "0100010111"

        Sets the bitset states to the states in the string
        '''

        if len(states) != len(self.bits):
            raise ValueError('The length of the given string and the size of the bitset do not match')
        
        for i, value in enumerate(states):

            index_state = value == '1'

            self.bits[i] = index_state