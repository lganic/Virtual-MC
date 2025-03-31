from .generic import Byteable_Object
from ..varint import write_var_int_bytes

class String(Byteable_Object, str):

    def to_bytes(self):
        
        encoded_string = str(self).encode('utf-8')

        return write_var_int_bytes(len(encoded_string)) + encoded_string