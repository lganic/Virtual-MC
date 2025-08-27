from virtual_mc.server.base import Server
from virtual_mc.server.states import State
from virtual_mc.data.types.numbers import Float, Double
import time
import os
os.system('cls')

k = Server()

print('Server is on!')

t = time.time()

while time.time() - t < 120:

    keys = list(k.clients.keys())

    for add in keys:

        if add not in k.clients:
            continue

        print(add, k.clients[add].current_handshake_state)

        if k.clients[add].current_handshake_state == State.PLAY:
            zero_double = Double(0).to_bytes()
            zero_float = Float(0).to_bytes()

            teleport_flags = b'\x00\x00\x00\x00'
            teleport_id = b'\x00'

            packet = b'\x41' + teleport_id + zero_double + zero_double + zero_double + zero_double + zero_double + zero_double + zero_float + zero_float + teleport_flags

            k.send(add, packet)
        
        time.sleep(1)

print('Server is off')