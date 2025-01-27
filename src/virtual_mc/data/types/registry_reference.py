from typing import Optional
from .generic import Byteable_Object
from ..var_int import write_var_int

class RegistryReference(Byteable_Object):
    
    def __init__(self, id = 0, value = None):

        self.id: int = id
        self.value: Optional[Byteable_Object] = value

    @staticmethod
    def from_reference(registry_id: int):
        '''
        Create a non-inline reference to a certain registry id
        '''

        id = registry_id + 1
        value = None

        return RegistryReference(id = id, value = value)
    
    @staticmethod
    def from_value(value: Byteable_Object):
        '''
        Create an inline reference using the given data
        '''

        id = 0
        value = value

        return RegistryReference(id = id, value = value)

    def to_bytes(self):
        
        if self.id == 0:
            # Inline. Encode value

            return bytes([0]) + self.value.to_bytes()
        
        return write_var_int(self.id)