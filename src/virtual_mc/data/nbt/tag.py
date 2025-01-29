
'''
Generic definition of NBT tag object
'''

from typing import Tuple, Any
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
    
    def parse_buffer(self, buffer: bytes, index: int, no_name: bool = False, no_type: bool = False) -> Tuple[Any, int]:
        """
        Parses an object from a bytes buffer starting at a specified index.

        Args:
            buffer (bytes): The bytes buffer containing the data to parse.
            index (int): The starting index within the buffer from which to begin parsing.
            no_name (bool, optional): Use if no name section is present
            no_type (bool, optional): Use if no type section is present

        Returns:
            Tuple[Any, int]: A tuple where the first element is the parsed object and the second
                            element is the number of bytes that were parsed.
        """

        raise NotImplementedError('This object has not implemented this function')