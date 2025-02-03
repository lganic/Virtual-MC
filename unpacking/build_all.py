from server_unpacker import cleanup, unpack_server
from build_block_state_ids import build_id_lookup

if __name__ == '__main__':

    unpack_server()

    build_id_lookup()

    cleanup()