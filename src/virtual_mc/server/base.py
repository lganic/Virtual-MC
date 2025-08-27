from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
import zlib
import socket
import threading
import json
import os
from typing import Tuple, List, Dict
from ..data.varint import read_var_int_bytes, read_var_long_bytes, get_length_var_int, write_var_int_bytes
from ..data.types import String, Boolean
from .utilities import get_server_protocol_version, get_server_version
from .parsing_utils import parse_00_packet, parse_01_packet, parse_02_packet, parse_07_packet
from .msg_types import Msg_Type
from .states import State
from .client import Client

COMPRESS_DATA = False
COMPRESSION_THRESHOLD = 256

def pack_n_send(connection, message: bytes, compress = False, encryption_cipher = None):

    # TODO : There is probably a cleaner implementation of this. 

    if not compress:
        message_len = len(message)

        message_var_int = write_var_int_bytes(message_len)

        full_packet = message_var_int + message

    else:
        original_length = len(message)

        if original_length < COMPRESSION_THRESHOLD:
            # Send uncompressed packet
            full_packet = b'\x00' + message

            message_len = len(full_packet)

            full_packet = write_var_int_bytes(message_len) + full_packet
        else:
            full_packet = write_var_int_bytes(original_length)

            full_packet += zlib.compress(message)

            full_packet = write_var_int_bytes(len(full_packet)) + full_packet

    if encryption_cipher is not None:
        full_packet = encryption_cipher.update(full_packet)

    connection.sendall(full_packet)

class Server:
    def __init__(self, port = 5290, max_players = 20, description = "A Minecraft Server"):

        self.port = port
        self.max_players = max_players
        self.description = description

        self.host = '0.0.0.0'
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        print(f"Server listening on {self.host}:{self.port}")
        self.running = True
        self.thread = threading.Thread(target=self._client_dispatcher, daemon = True)
        self.thread.start()

        self.client_connections = {}
        self.client_addresses = {}
        self.active_client_threads = {}
        self.clients: Dict[str, Client] = {}

        self.encrypt_ciphers = {}
        self.decrypt_ciphers = {} 

        # Generate RSA keypair (do this once on server startup)
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=1024)

        # DER-encoded public key (ASN.1 SubjectPublicKeyInfo)
        self.public_key_der = self.private_key.public_key().public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )


    def _client_dispatcher(self):

        while self.running:
            client_conn, client_addr = self.sock.accept()
            print(f'Accepted a connection: {client_addr}')

            handler_thread = threading.Thread(
                target=self._run_client_handler,
                args=(client_conn, client_addr),
                daemon=True
            )
            handler_thread.start()

            composite_address = client_addr[0] + ':' + str(client_addr[1])

            self.active_client_threads[composite_address] = handler_thread

    def _run_client_handler(self, connection, address):

        connection.setblocking(False)
        connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        incoming_data_buffer = b''
        force_read_packet = False

        print(f'Running a client handler on address: {address}')

        composite_address = address[0] + ':' + str(address[1])

        client_object = Client()
        client_object.current_handshake_state = State.STATUS

        self.client_addresses[composite_address] = address
        self.client_connections[composite_address] = connection
        self.clients[composite_address] = client_object
        self.encrypt_ciphers[composite_address] = None
        self.decrypt_ciphers[composite_address] = None

        verify_token = os.urandom(16)

        traffic_encrypted = False
        traffic_compressed = False

        plugin_identifier = None
        plugin_data = None

        try:
            while self.running:

                data = b'' # Clear incoming data buffer

                try:
                    data = connection.recv(1024)
                except BlockingIOError:
                    if not force_read_packet:
                        continue

                if data and traffic_encrypted:
                    data = decrypt_cipher.update(data)

                if not (data or force_read_packet):
                    continue

                force_read_packet = False

                incoming_data_buffer += data

                var_int_length = get_length_var_int(incoming_data_buffer)
                if var_int_length != -1:
                    
                    # Full varint recieved, read the value, which represents the length of the incoming packet

                    packet_length_varint = incoming_data_buffer[:var_int_length]
                    packet_length = read_var_int_bytes(packet_length_varint)

                    if len(incoming_data_buffer) >= packet_length + var_int_length:
                        # We have recieved the full number of bytes. Isolate the packet, and continue
                        packet = incoming_data_buffer[var_int_length: packet_length + var_int_length]
                        incoming_data_buffer = incoming_data_buffer[packet_length + var_int_length:]

                        print(client_object.current_handshake_state, f'Received full packet: {packet}')

                        if incoming_data_buffer:
                            # We just read some data, and updated the buffer, but there are still bytes in waiting. Signal the loop to read immediately, to check if another valid packet is in waiting. 
                            force_read_packet = True

                        if packet[0] == 0:

                            message_type, content = parse_00_packet(packet, client_object.current_handshake_state)

                            if message_type == Msg_Type.SERVER_PING:
                                pack_n_send(connection, b'\x00' + self.generate_server_json(), compress=traffic_compressed, encryption_cipher=self.encrypt_ciphers[composite_address])
                                continue

                            if message_type == Msg_Type.HANDSHAKE:
                                prot_vesion, serv_addr, serv_port, next_state = content

                                client_object.prot_version = prot_vesion
                                client_object.address = serv_addr
                                client_object.port = serv_port
                                client_object.current_handshake_state = next_state

                            if message_type == Msg_Type.LOGIN:
                                print(client_object.current_handshake_state, 'Login request detected: ', content)
                                client_object.username = content[0]
                                client_object.user_uuid = content[1]

                                # Respond with the encryption packet. 
                                server_id_bytes = b'\x00' # Empty string
                                public_key_bytes = write_var_int_bytes(len(self.public_key_der)) + self.public_key_der
                                verify_token_bytes = write_var_int_bytes(len(verify_token)) + verify_token
                                should_auth = Boolean(False).to_bytes()

                                enc_packet = b'\x01' + server_id_bytes + public_key_bytes + verify_token_bytes + should_auth
                                
                                pack_n_send(connection, enc_packet, compress=traffic_compressed, encryption_cipher=self.encrypt_ciphers[composite_address])
                                continue

                            if message_type == Msg_Type.CLIENT_CONFIG:
                                locale, view_distance, _, _, _, _, _, _, _ = content

                                client_object.locale = locale
                                client_object.view_distance = view_distance

                            continue

                        elif packet[0] == 1:
                            message_type, content = parse_01_packet(packet, client_object.current_handshake_state)

                            if message_type == Msg_Type.PING:
                                pack_n_send(connection, content[0], compress=traffic_compressed, encryption_cipher=self.encrypt_ciphers[composite_address])
                            
                            if message_type == Msg_Type.ENCRYPTION:
                                
                                encrypted_shared_secret, encrypted_verify_token = content

                                shared_secret = self.private_key.decrypt(
                                    encrypted_shared_secret,
                                    padding=padding.PKCS1v15()
                                )

                                decrypted_verify_token = self.private_key.decrypt(
                                    encrypted_verify_token,
                                    padding=padding.PKCS1v15()
                                )

                                # Now compare
                                if decrypted_verify_token != verify_token:
                                    print(client_object.current_handshake_state, "Verify token mismatch! Possible MITM attack or protocol error.")
                                    print(client_object.current_handshake_state, "Terminating connection immediately")
                                    break

                                encrypt_cipher = Cipher(
                                    algorithms.AES(shared_secret),
                                    modes.CFB8(shared_secret),
                                    backend=default_backend()
                                ).encryptor()

                                decrypt_cipher = Cipher(
                                    algorithms.AES(shared_secret),
                                    modes.CFB8(shared_secret),
                                    backend=default_backend()
                                ).decryptor()

                                traffic_encrypted = True
                                self.encrypt_ciphers[composite_address] = encrypt_cipher
                                print(client_object.current_handshake_state, "Traffic now encrypted")

                                if COMPRESS_DATA:
                                    print(client_object.current_handshake_state, "Sending compression start.")
                                    # Send a compression start command
                                    compression_start = b'\x03' + write_var_int_bytes(COMPRESSION_THRESHOLD)
                                    pack_n_send(connection, compression_start, compress=traffic_compressed, encryption_cipher=self.encrypt_ciphers[composite_address])

                                    print(client_object.current_handshake_state, "Traffic now compressed")
                                    traffic_compressed = True

                                # Create, and respond with the players login success.

                                print(client_object.current_handshake_state, "Sending good login")
                                client_username = String(client_object.username.decode())
                                login_sucess = b'\x02' + client_object.user_uuid.bytes + client_username.to_bytes() + b'\x00' # TODO : Finish the rest of this prefixed list. 
                                pack_n_send(connection, login_sucess, compress=traffic_compressed, encryption_cipher=self.encrypt_ciphers[composite_address])
                        
                        elif packet[0] == 2:
                            message_type, content = parse_02_packet(packet, client_object.current_handshake_state)

                            if message_type == Msg_Type.PLUGIN_MSG:
                                plugin_identifier = content[0]
                                plugin_data = content[1]

                        elif packet[0] == 3:
                            if client_object.current_handshake_state == State.LOGIN:
                                # Configuration packet. 

                                client_object.current_handshake_state = State.CONFIGURATION

                                # What follows this is the clientbound known packs. Send it now. 

                                known_packs_packet = b'\x0E\x01' + String("minecraft").to_bytes() + String("core").to_bytes() + String(get_server_version()).to_bytes()

                                pack_n_send(connection, known_packs_packet, compress=traffic_compressed, encryption_cipher=self.encrypt_ciphers[composite_address])

                            elif client_object.current_handshake_state == State.CONFIGURATION:
                                # Play packet

                                client_object.current_handshake_state = State.PLAY

                            print(client_object.current_handshake_state, "03 state transition", client_object.current_handshake_state)

                        elif packet[0] == 7:
                            message_type, content = parse_07_packet(packet, client_object.current_handshake_state)

                            if message_type == Msg_Type.KNOWN_PACKS_MSG:

                                packs = content[0]

                                # Make sure that the client is reporting a bog standard install. 
                                if len(packs) != 1:
                                    print("Client is reporting datapacks, which aren't supported.")
                                    break # Stop the connection

                                if packs[0][0] != "minecraft" and packs[0][1] != "core" and packs[0][2] != get_server_version():
                                    print(f"Client a datapack that is not valid: {packs}")
                                    break # Stop the connection     

                                # This packet means we have received all the required config info. Send the end config packet
                                pack_n_send(connection, b'\x03', compress=traffic_compressed, encryption_cipher=self.encrypt_ciphers[composite_address])                               

                        else:
                            raise NotImplementedError("Packet not recognized by any known type.")

                        packet = b''


        except (ConnectionResetError, ConnectionAbortedError):
            print(client_object.current_handshake_state, "Client disconnected abruptly.")
        finally:
            connection.close()
            print(client_object.current_handshake_state, f"Connection with {address} closed.")

            # Find the address in the list, and remove the thread, and the connection from the list. 
            connection_index = self.client_addresses.index(address)

            self.client_connections.pop(connection_index)
            self.client_addresses.pop(connection_index)
            self.active_client_threads.pop(connection_index)
            print(client_object.current_handshake_state, "Client was cleaned up")

    def generate_server_json(self):
        server_data = {
            'version': {'name': get_server_version(), 'protocol': get_server_protocol_version()},
            'enforcesSecureChat': True,
            'description': self.description,
            # 'description': {'text': self.description},
            'players': {'max': self.max_players, 'online': len(self.client_connections) - 1} # Do -1 since one of the active connections is the one asking for this packet
        }

        packed_json_data = json.dumps(server_data, separators=(',', ':'))

        string_object = String(packed_json_data)

        return string_object.to_bytes()

    def send(self, client_composite_address, data):

        pack_n_send(self.client_connections[client_composite_address], data, False, self.encrypt_ciphers[client_composite_address])

    def close(self):
        self.running = False
        if self.client_conn:
            self.client_conn.close()
        self.sock.close()
        print("Server shut down.")