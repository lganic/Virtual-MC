
'''
Generic definition of NBT tag object
'''

from typing import Tuple, Any, Type
from .nbt_util import encode_short, decode_short

def _check_type_at_buffer_index(buffer, index, expected_type):

    type_num = buffer[index]

    if type_num != expected_type:
        raise TypeError(f'Decoded type: {type_num} is not expected object type: {expected_type} at index: {index}')

def _read_name_at_buffer_index(buffer: bytes, index: int):

    name_length = decode_short(buffer[index: index + 2])

    name_bytes: bytes = buffer[index + 2: index + name_length + 2]

    parsed = 2 + name_length

    name = name_bytes.decode()

    return (name, parsed)

class NBT_Tag:
    
    default_type: int

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
    
    def pretty_tree(self, indent=0):
        raise NotImplementedError('pretty tree is not implemented for object type!')

    def tag_info(self):
        # Trying to mimic PyNBT debug outout format here:

        return f"{self.__class__.__name__}('{self.name}'): "
    
    @classmethod
    def parse_buffer(cls: Type['NBT_Tag'], buffer: bytes, index: int, no_name: bool = False, no_type: bool = False) -> Tuple[str, Any, int]:
        """
        Parses an object from a bytes buffer starting at a specified index.

        Args:
            buffer (bytes): The bytes buffer containing the data to parse.
            index (int): The starting index within the buffer from which to begin parsing.
            no_name (bool, optional): Use if no name section is present
            no_type (bool, optional): Use if no type section is present

        Returns:
            Tuple[str, Any, int]: A tuple where the first element is the object name,
                            the second is the parsed object
                            the last element is the number of bytes that were parsed.
        """

        parsed = 0

        if not no_type:

            _check_type_at_buffer_index(buffer, index, cls.default_type)

            index += 1
            parsed += 1
        
        name = ''

        if not no_name:

            name, name_length = _read_name_at_buffer_index(buffer, index)

            index += name_length
            parsed += name_length
        
        payload = cls.parse_payload(name, buffer, index)

        return (name, payload[0], parsed + payload[1])

    @classmethod
    def parse_payload(self, name: str, buffer: bytes, index: int) -> Tuple[Any, int]:

        raise NotImplementedError('Parse payload is not implemented for object type!')