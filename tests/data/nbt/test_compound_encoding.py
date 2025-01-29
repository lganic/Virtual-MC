import pytest
from virtual_mc.data.nbt.nbt_types import NBT_Compound, NBT_String


def test_bananarama():

    root_name = 'hello world'
    string_name = 'name'
    string_content = 'Bananrama'

    root_object = NBT_Compound(root_name)

    string_object = NBT_String(string_name, string_content)

    root_object.objects.append(string_object)

    result = root_object.to_bytes()

    expected = bytes([0x0a,0x00,0x0b,0x68,0x65,0x6c,0x6c,0x6f,0x20,0x77,0x6f,0x72,0x6c,0x64,0x08,0x00,0x04,0x6e ,0x61,0x6d,0x65,0x00,0x09,0x42,0x61,0x6e,0x61,0x6e,0x72,0x61,0x6d,0x61,0x00])

    print('Result:   ', result)
    print('Expected: ', expected)

    assert result == expected