import os
from .server_unpacker import cleanup, unpack_server, get_most_recent_version
from .build_block_state_ids import build_id_lookup

VERSION_PATH = os.path.join(os.path.dirname(__file__), '../../../data/server_version.txt')

def build_all():

    unpack_server()

    build_id_lookup()

    cleanup()

    print('Updating server_version.txt')
    most_recent_version = get_most_recent_version()

    with open(VERSION_PATH, 'w') as f:
        f.write(most_recent_version)

    print('Done!')


if __name__ == '__main__':
    build_all()