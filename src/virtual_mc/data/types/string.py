from .generic import Byteable_Object
from ..var_int import write_var_int

class String(Byteable_Object, str):

    def to_bytes(self):
        
        encoded_string = str(self).encode('utf-8')

        return write_var_int(len(encoded_string)) + encoded_string