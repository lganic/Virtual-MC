from .generic import Byteable_Object
from .string import String
from .array import Array
from ..varint import write_var_int_bytes
from .numbers import VarInt

class IdSet(Byteable_Object):

    def __init__(self, type: int, tag_name: None, ids = []):

        self.type = type
        self.tag_name = tag_name
        self.ids = ids
    
    def to_bytes(self) -> bytes: 
        
        type_bytes = write_var_int_bytes(self.type)

        if self.type == 0:

            # Return identifier

            tag_object = String(self.tag_name)

            return type_bytes + tag_object.to_bytes()
        
        if len(self.ids) != self.type - 1:
            raise ValueError('Size mismatch, id array length must be equal to type - 1')
    
        id_array = Array()

        for id in self.ids:

            id_array.add_object(VarInt(id))
        
        return type_bytes + id_array.to_bytes()