import os
import json

from .server_unpacker import cleanup, unpack_server, get_most_recent_version, server_abspath
from .build_block_state_ids import build_id_lookup
from .read_version_json import read_version_json

VERSION_PATH = os.path.join(os.path.dirname(__file__), '../../../data/server_version.json')

def build_all():

    unpack_server()

    server_version_info = read_version_json(server_abspath)
    server_protocol_version = server_version_info['protocol_version']

    build_id_lookup()

    cleanup()

    print('Updating server_version.json')
    most_recent_version = get_most_recent_version()

    digest = {
        'server_version': most_recent_version,
        'protocol_version': server_protocol_version
    }

    with open(VERSION_PATH, 'w') as f:
        json.dump(digest, f)

    print('Done!')


if __name__ == '__main__':
    build_all()