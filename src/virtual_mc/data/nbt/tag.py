
'''
Generic definition of NBT tag object
'''

from .nbt_util import encode_short

class NBT_Tag:
    
    def __init__(self, type: int, name: str, is_network: bool = False):

        self.type = type
        self.name = name

        self.is_network = is_network
    
    def payload(self):

        raise NotImplementedError('Payload is not implemented for object type!')

    def to_bytes(self):

        base = bytes([self.type])

        if not self.is_network:

            name_bytes = self.name.encode()

            base += encode_short(len(name_bytes)) + name_bytes
        
        return base + self.payload()