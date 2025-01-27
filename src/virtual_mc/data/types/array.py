from typing import List

from .generic import Byteable_Object
from ..var_int import write_var_int

class Array(Byteable_Object):

    objects: List[Byteable_Object]

    def __init__(self):
        self.objects = list()

    def to_bytes(self) -> bytes:
        
        output = bytes() # No length for generic arrays

        for obj in self.objects:
            output += obj.to_bytes()
        
        return output

    def add_object(self, obj: Byteable_Object):

        self.objects.append(obj)

class PrefixedArray(Array):

    def __init__(self):
        super().__init__()
    
    def to_bytes(self):

        # Fetch array bytes
        base_output = super().to_bytes()

        # Add varint length to packet
        length_varint = write_var_int(len(base_output))

        return length_varint + base_output