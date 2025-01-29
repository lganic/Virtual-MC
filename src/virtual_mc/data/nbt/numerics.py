from struct import Struct
from typing import Union
from .tag import NBT_Tag
from .type_ids import TAG_BYTE, TAG_SHORT, TAG_INT, TAG_LONG, TAG_FLOAT, TAG_DOUBLE

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

class TAG_Byte(NBT_Numeric):
    """Represent a single tag storing 1 byte."""
    default_type = TAG_BYTE
    fmt = Struct(">b")


class TAG_Short(NBT_Numeric):
    """Represent a single tag storing 1 short."""
    id = TAG_SHORT
    fmt = Struct(">h")


class TAG_Int(NBT_Numeric):
    """Represent a single tag storing 1 int."""
    id = TAG_INT
    fmt = Struct(">i")
    """Struct(">i"), 32-bits integer, big-endian"""


class TAG_Long(NBT_Numeric):
    """Represent a single tag storing 1 long."""
    id = TAG_LONG
    fmt = Struct(">q")


class TAG_Float(NBT_Numeric):
    """Represent a single tag storing 1 IEEE-754 floating point number."""
    id = TAG_FLOAT
    fmt = Struct(">f")


class TAG_Double(NBT_Numeric):
    """Represent a single tag storing 1 IEEE-754 double precision floating
    point number."""
    id = TAG_DOUBLE
    fmt = Struct(">d")