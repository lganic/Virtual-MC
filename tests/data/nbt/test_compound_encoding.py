import pytest
import os
from virtual_mc.data.nbt.nbt_types import NBT_Compound, NBT_String
import gzip


def test_bananarama():

    root_name = 'hello world'
    string_name = 'name'
    string_content = 'Bananrama'

    root_object = NBT_Compound(root_name)

    string_object = NBT_String(string_name, string_content)

    root_object.objects.append(string_object)

    result = root_object.to_bytes()

    expected = bytes([0x0a,0x00,0x0b,0x68,0x65,0x6c,0x6c,0x6f,0x20,0x77,0x6f,0x72,0x6c,0x64,0x08,0x00,0x04,0x6e ,0x61,0x6d,0x65,0x00,0x09,0x42,0x61,0x6e,0x61,0x6e,0x72,0x61,0x6d,0x61,0x00])

    assert result == expected

def test_hello_world_nbt():

    # Load hello world NBT

    with open(os.path.join(os.path.dirname(__file__), 'hello_world.nbt') , 'rb') as f:
        contents = f.read()
    
    result = name, object, size = NBT_Compound.parse_buffer(contents, 0)

    object: NBT_Compound

    assert object.pretty_tree() == "NBT_Compound('hello world'): 1 entry\n{\n\tNBT_String('name'): Bananrama\n}\n"

    recoded = object.to_bytes()

    assert object.is_network == False

    assert contents == recoded

def test_bigtest_nbt():

    # Load hello world NBT

    with open(os.path.join(os.path.dirname(__file__), 'bigtest.nbt') , 'rb') as f:
        contents = f.read()

    contents = gzip.decompress(contents)

    result = name, object, size = NBT_Compound.parse_buffer(contents, 0)

    object: NBT_Compound

    recoded = object.to_bytes()

    assert object.is_network == False

    assert contents == recoded