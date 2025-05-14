import json
import os

server_version_abspath = os.path.join(os.path.dirname(__file__), '../../../data/server_version.json')

def _get_version_info():

    with open(server_version_abspath, 'r') as server_version_file:
        return json.load(server_version_file)


def get_server_protocol_version():

    v_info = _get_version_info()

    return v_info['protocol_version']

def get_server_version():

    v_info = _get_version_info()

    return v_info['server_version']

