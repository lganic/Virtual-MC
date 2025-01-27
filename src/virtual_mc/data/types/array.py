from typing import List

from .generic import Byteable_Object

class Array(Byteable_Object):

    objects: List[Byteable_Object]

    def to_bytes(self) -> bytes:
        
        output = bytes() # No length for generic arrays

        for obj in self.objects:
            output += obj.to_bytes()
        
        return output

    def add_object(self, obj: Byteable_Object):

        self.objects.append(obj)