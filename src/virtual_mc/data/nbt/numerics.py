from struct import Struct
from typing import Union, List
from .tag import NBT_Tag
from .type_ids import TAG_BYTE, TAG_SHORT, TAG_INT, TAG_LONG, TAG_FLOAT, TAG_DOUBLE, TAG_END, TAG_COMPOUND

class NBT_Numeric(NBT_Tag):
    """comparable to int with an intrinsic name"""

    fmt : Struct
    default_type : int

    value: Union[float, int]

    def __init__(self, value, name):
        super().__init__(self.default_type, name)

        self.value = value

    def payload(self):

        return self.fmt.pack(self.value)

class NBT_Byte(NBT_Numeric):
    """Represent a single tag storing 1 byte."""
    default_type = TAG_BYTE
    fmt = Struct(">b")


class NBT_Short(NBT_Numeric):
    """Represent a single tag storing 1 short."""
    id = TAG_SHORT
    fmt = Struct(">h")


class NBT_Int(NBT_Numeric):
    """Represent a single tag storing 1 int."""
    id = TAG_INT
    fmt = Struct(">i")
    """Struct(">i"), 32-bits integer, big-endian"""


class NBT_Long(NBT_Numeric):
    """Represent a single tag storing 1 long."""
    id = TAG_LONG
    fmt = Struct(">q")


class NBT_Float(NBT_Numeric):
    """Represent a single tag storing 1 IEEE-754 floating point number."""
    id = TAG_FLOAT
    fmt = Struct(">f")


class NBT_Double(NBT_Numeric):
    """Represent a single tag storing 1 IEEE-754 double precision floating
    point number."""
    id = TAG_DOUBLE
    fmt = Struct(">d")

class NBT_End(NBT_Tag):

    def __init__(self):
        super().__init__(TAG_END, '')
    
    def payload(self):
        return bytes()

class NBT_Compound(NBT_Tag):

    def __init__(self, name, is_network = False):
        super().__init__(NBT_Compound, name, is_network = is_network)

        self.objects: List[NBT_Tag] = []
    
    def payload(self):

        output_bytes = bytes()

        for obj in self.objects + [NBT_End()]:

            output_bytes += obj.to_bytes()
        
        return output_bytes