import gzip
from .nbt_types import NBT_Compound

def parse_byte_string(buffer: bytes, is_network = False) -> NBT_Compound:

    '''
    Parse a given byte string for NBT data

    Note that this function expects that the given byte string represents the entire NBT file. 
    '''

    name, object, size = NBT_Compound.parse_buffer(buffer, 0, no_name = is_network)

    return object

def parse_compressed_byte_string(compressed_buffer: bytes, is_network = False) -> NBT_Compound:

    '''
    Parse a given compressed byte string for NBT data

    Note that this function expects that the given byte string represents the entire NBT file. 
    '''

    decompressed_content = gzip.decompress(compressed_buffer)

    return parse_byte_string(decompressed_content, is_network = is_network)

def parse_file(file_path: str) -> NBT_Compound:

    '''
    Open and parse a NBT file which is not compressed
    '''

    with open(file_path, 'rb') as binary_file:

        byte_buffer = binary_file.read()

    return parse_byte_string(byte_buffer)

def parse_compressed_file(file_path: str) -> NBT_Compound:

    '''
    Open and parse a NBT file which is compressed
    '''

    with open(file_path, 'rb') as binary_file:

        compressed_buffer = binary_file.read()
    
    return parse_compressed_byte_string(compressed_buffer)
