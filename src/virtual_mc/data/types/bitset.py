from .generic import Byteable_Object
from .numbers import Long
from .array import Array
from ..varint import write_var_int_bytes

# NOTE : There are a bunch of assumptions I am making here because the doc is a little unclear on the specifics of ordering, and if the encoded longs should have 2s complement. 
# So do be warned, these might not work right now! I'm going to revisit these later once I've done a little more research. 

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
            long_value = int("".join(str(int(bit)) for bit in chunk[::-1]), 2)  # Convert reversed chunk into binary string and then to an integer

            output_array.append(long_value)
        
        return output_array

    def to_bytes(self):

        output_array = Array()

        long_array = self.to_long_array()

        for long_value in long_array:

            output_array.add_object(Long(long_value))
        
        num_longs = len(long_array)

        print(output_array.to_bytes())

        return write_var_int_bytes(num_longs) + output_array.to_bytes()
    
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

    def __setitem__(self, index, value):
        if isinstance(index, slice):  # Handle slicing
            if len(value) != (index.stop - index.start):
                raise ValueError("Slice length and values length must match")
            for i, val in zip(range(index.start, index.stop), value):
                self.bits[i] = val == '1'
        else:  # Handle single index

            if len(value) != 1:
                raise ValueError('Invalid value size for single index set')

            self.bits[index] = value == '1'