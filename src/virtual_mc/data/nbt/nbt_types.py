from struct import Struct
from typing import Union, List
from .tag import NBT_Tag
from .type_ids import TAG_END, TAG_BYTE, TAG_SHORT, TAG_INT, TAG_LONG, TAG_FLOAT, TAG_DOUBLE, TAG_BYTE_ARRAY, TAG_STRING, TAG_LIST, TAG_COMPOUND, TAG_INT_ARRAY, TAG_LONG_ARRAY
from .nbt_util import encode_short, encode_int

class _NBT_Numeric(NBT_Tag):
    """comparable to int with an intrinsic name"""

    fmt : Struct
    default_type : int

    value: Union[float, int]

    def __init__(self, value, name):
        super().__init__(self.default_type, name)

        self.value = value

    def payload(self):

        return self.fmt.pack(self.value)

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

    def __init__(self):
        super().__init__(TAG_END, '', is_network=True) # The is_network here isn't part of the spec, just a hacky trick
    
    def payload(self):
        return bytes()

class NBT_Compound(NBT_Tag):

    def __init__(self, name, is_network = False):
        super().__init__(TAG_COMPOUND, name, is_network = is_network)

        self.objects: List[NBT_Tag] = []
    
    def payload(self):

        output_bytes = bytes()

        for obj in self.objects + [NBT_End()]:

            output_bytes += obj.to_bytes()
        
        return output_bytes

class NBT_String(NBT_Tag):

    def __init__(self, name: str, value: str):
        super().__init__(TAG_STRING, name)

        self.value = value
    
    def payload(self):
        
        s_bytes = self.value.encode()

        num_bytes = len(s_bytes)

        return encode_short(num_bytes) + s_bytes

class _NBT_Length_Prefixed_Array(NBT_Tag):

    objects: List[NBT_Tag]
    default_type: int

    def __init__(self, name):
        super().__init__(self.default_type, name)

    def payload(self):

        array_length = len(self.objects)

        output_bytes = encode_int(array_length)

        for obj in self.objects:
            output_bytes += obj.payload() # Ignore name
        
        return output_bytes

class NBT_ByteArray(_NBT_Length_Prefixed_Array):

    objects: List[NBT_Byte]
    default_type = TAG_BYTE_ARRAY

class NBT_IntArray(_NBT_Length_Prefixed_Array):

    objects: List[NBT_Int]
    default_type = TAG_INT_ARRAY

class NBT_LongArray(_NBT_Length_Prefixed_Array):

    objects: List[NBT_Long]
    default_type = TAG_LONG_ARRAY
