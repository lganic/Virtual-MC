from struct import Struct
from typing import Union, List, Type
from .tag import NBT_Tag
from .type_ids import TAG_END, TAG_BYTE, TAG_SHORT, TAG_INT, TAG_LONG, TAG_FLOAT, TAG_DOUBLE, TAG_BYTE_ARRAY, TAG_STRING, TAG_LIST, TAG_COMPOUND, TAG_INT_ARRAY, TAG_LONG_ARRAY
from .nbt_util import encode_short, encode_int, decode_short, decode_int

class _NBT_Numeric(NBT_Tag):
    """comparable to int with an intrinsic name"""

    fmt : Struct

    value: Union[float, int]

    def __init__(self, name, value):
        super().__init__(self.default_type, name)

        self.value = value

    def payload(self):

        return self.fmt.pack(self.value)

    @classmethod
    def parse_payload(cls, name: str, buffer: bytes, index: int, no_name = False, no_type = False):

        num_to_decode = cls.fmt.size

        value_bytes = buffer[index: index + num_to_decode]

        result = cls.fmt.unpack(value_bytes)

        ret_obj = cls(name, result)

        return (ret_obj, num_to_decode)
    
    def pretty_tree(self, indent=0):
        """Return formated Unicode string of self, where iterable items are
        recursively listed in detail."""
        return ("\t" * indent) + self.tag_info() + str(self.value) + '\n'

class NBT_Byte(_NBT_Numeric):
    """Represent a single tag storing 1 byte."""
    default_type = TAG_BYTE
    fmt = Struct(">b")


class NBT_Short(_NBT_Numeric):
    """Represent a single tag storing 1 short."""
    default_type = TAG_SHORT
    fmt = Struct(">h")


class NBT_Int(_NBT_Numeric):
    """Represent a single tag storing 1 int."""
    default_type = TAG_INT
    fmt = Struct(">i")
    """Struct(">i"), 32-bits integer, big-endian"""


class NBT_Long(_NBT_Numeric):
    """Represent a single tag storing 1 long."""
    default_type = TAG_LONG
    fmt = Struct(">q")


class NBT_Float(_NBT_Numeric):
    """Represent a single tag storing 1 IEEE-754 floating point number."""
    default_type = TAG_FLOAT
    fmt = Struct(">f")


class NBT_Double(_NBT_Numeric):
    """Represent a single tag storing 1 IEEE-754 double precision floating
    point number."""
    default_type = TAG_DOUBLE
    fmt = Struct(">d")

class NBT_End(NBT_Tag):

    default_type = TAG_END

    def __init__(self):
        super().__init__(TAG_END, '', is_network=True) # The is_network here isn't part of the spec, just a hacky trick
    
    def payload(self):
        return bytes()
    
    @classmethod
    def parse_buffer(cls, buffer, index, no_name = False, no_type = False):

        return ('', cls(), 1)

class _NBT_Group(NBT_Tag):

    objects: List[NBT_Tag]

    def pretty_tree(self, indent=0):
        """Return formated Unicode string of self, where iterable items are
        recursively listed in detail."""
        
        output = ("\t" * indent) + self.tag_info() + str(len(self.objects))+ ' entries\n' + ("\t" * indent) + '{\n'

        for item in self.objects:
            output += item.pretty_tree(indent + 1)
        
        output += ("\t" * indent) + '}\n'

        return output

class NBT_Compound(_NBT_Group):

    default_type = TAG_COMPOUND

    def __init__(self, name, is_network = False, objects: List[NBT_Tag] = list()):
        super().__init__(self.default_type, name, is_network = is_network)

        self.objects: List[NBT_Tag] = objects
    
    def payload(self):

        output_bytes = bytes()

        for obj in self.objects + [NBT_End()]:

            output_bytes += obj.to_bytes()
        
        return output_bytes
    
    @classmethod
    def parse_payload(cls, name: str, buffer: bytes, index: int):

        parsed_objects = []
        parsed_bytes = 0

        while True:

            object_type_value = buffer[index]
            object_type: NBT_Tag = TAG_TABLE[object_type_value]

            if object_type == NBT_End:
                parsed_bytes += 1
                break

            _, object, size = object_type.parse_buffer(buffer, index)

            parsed_objects.append(object)

            index += size
            parsed_bytes += size
        
        network = False

        if name == '':
            # Probably a network compound
            network = True

        output_compound: NBT_Compound = cls(name, is_network = True, objects = parsed_objects)

        return output_compound, parsed_bytes

class NBT_String(NBT_Tag):
    
    default_type = TAG_STRING

    def __init__(self, name: str, value: str):
        super().__init__(self.default_type, name)

        self.value = value
    
    def payload(self):
        
        s_bytes = self.value.encode()

        num_bytes = len(s_bytes)

        return encode_short(num_bytes) + s_bytes
    
    @classmethod
    def parse_payload(cls, name: str, buffer: bytes, index: int):

        string_length = decode_short(buffer[index: index + 2])

        string_bytes = buffer[index + 2: index + 2 + string_length]

        string_value = string_bytes.decode()

        output_obj = cls(name, string_value)

        return output_obj, 2 + string_length
    
    def pretty_tree(self, indent=0):
        
        return ('\t' * indent) + self.tag_info() + self.value + '\n'

class _NBT_Length_Prefixed_Array(_NBT_Group):

    object_type: NBT_Tag

    def __init__(self, name: str, objects: List[NBT_Tag] = list()):
        super().__init__(self.default_type, name)

        self.objects = objects

    def payload(self):

        array_length = len(self.objects)

        output_bytes = encode_int(array_length)

        for obj in self.objects:

            if not isinstance(obj, self.object_type):
                raise TypeError(f'An object int the array is not of expected type: {obj}')

            output_bytes += obj.payload() # Ignore name, and type
        
        return output_bytes
    
    @classmethod
    def parse_payload(cls, name: str, buffer: bytes, index: int):

        # Find the number of objects in the array
        length_bytes = buffer[index: index + 4]
        index += 4

        array_length = decode_int(length_bytes)

        parsed_bytes = 4
        output_objects = []

        for _ in range(array_length):

            obj_name, obj, size = cls.object_type.parse_buffer(buffer, index, no_name = True, no_type = True)

            output_objects.append(obj)

            index += size
            parsed_bytes += size
        
        output_array = cls(name, objects = output_objects)

        return output_array, parsed_bytes

class NBT_ByteArray(_NBT_Length_Prefixed_Array):

    objects: List[NBT_Byte]
    object_type: NBT_Byte
    default_type = TAG_BYTE_ARRAY

class NBT_IntArray(_NBT_Length_Prefixed_Array):

    objects: List[NBT_Int]
    object_type: NBT_Int
    default_type = TAG_INT_ARRAY

class NBT_LongArray(_NBT_Length_Prefixed_Array):

    objects: List[NBT_Long]
    object_type: NBT_Long
    default_type = TAG_LONG_ARRAY

class NBT_List(_NBT_Length_Prefixed_Array):

    default_type = TAG_LIST

    def __init__(self, name, object_type, objects: List[NBT_Tag] = []):

        self.object_type = object_type

        super().__init__(name, objects = objects)
    
    def payload(self):

        if len(self.objects) == 0:

            base = bytes([TAG_END]) # Empty array, use end tag for type rather than object type
        
        else:

            base = bytes([self.object_type])

        return base + super().payload()

    @classmethod
    def parse_payload(cls, name: str, buffer: bytes, index: int):

        # Find the object type contained in the array
        object_id_value = buffer[index]
        index += 1

        # Find the number of objects in the array
        length_bytes = buffer[index: index + 4]
        index += 4

        object_type: Type[NBT_Tag] = TAG_TABLE[object_id_value]

        array_length = decode_int(length_bytes)

        parsed_bytes = 5
        output_objects = []

        for _ in range(array_length):

            obj_name, obj, size = object_type.parse_buffer(buffer, index, no_name = True, no_type = True)

            output_objects.append(obj)

            index += size
            parsed_bytes += size
        
        output_array = cls(name, object_type = object_type, objects = output_objects)

        return output_array, parsed_bytes

TAG_TABLE = {TAG_END: NBT_End, TAG_END: NBT_End, TAG_BYTE: NBT_Byte, TAG_SHORT: NBT_Short, TAG_INT: NBT_Int, TAG_LONG: NBT_Long, TAG_FLOAT: NBT_Float, TAG_DOUBLE: NBT_Double, TAG_BYTE_ARRAY: NBT_ByteArray, TAG_STRING: NBT_String, TAG_LIST: NBT_List, TAG_COMPOUND: NBT_Compound, TAG_INT_ARRAY: NBT_IntArray, TAG_LONG_ARRAY: NBT_LongArray}
