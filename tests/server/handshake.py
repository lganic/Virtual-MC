import pytest
from virtual_mc.server.handshake import parse_handshake

def test_parse_sample_handshake():

    prot_vers, serv_address, serv_port, next_state = parse_handshake(b'\x00\x82\x06\r192.168.0.184\x14\xaa\x01')

    print(prot_vers, serv_address, serv_port, next_state)