import socket
import threading
import sys
import random


class VirtualRoom:
    def __init__(self, identificativo, client1, client2, server):
        self.identificativo = identificativo
        self.white = client1
        self.black = client2
        self.room_proprietary = server
    
    @staticmethod
    def generate_random_id(n_size, taken_id):
        random_id = ""
        i = 0
        while i < n_size:
            n1 = random.randint(0, 9)
            r = random.randint(0, 26)
            k = random.randint(0, 26)
            chosen_letter = chr(((k - r) % 26) + 97).upper()
            random_id += f"{n1}{chosen_letter}"
            i += 1
        
        if random_id in taken_id:
            return VirtualRoom.generate_random_id(n_size, taken_id)
        
        return random_id


class PyChessServer:

    SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, ip_address, port, max_connession_refused):
        self.ip_address = ip_address
        self.port = port
        self.max_conn_ref = max_connession_refused
        self.connected_host = 0
        self.connection_pool = dict()
        self.start()
    
    def start(self):
        self.SOCKET.bind((self.ip_address, self.port))
        self.SOCKET.listen(self.max_conn_ref)

    def rcv_message_from_client(self, client_name, connection_obj, client_address):
        while (msg := connection_obj.recv(4096).decode("utf-8")):
            print(f"Messaggio da {client_address} -> {msg}")
        self.connected_host -= 1
        self.connection_pool.pop(client_name)

    def accept_connections(self):
        while True:
            client_socket, client_address = self.SOCKET.accept()
            client_name = client_socket.recv(4096).decode("utf-8")
            self.connection_pool[client_name] = (client_socket, client_address)
            print(self.connection_pool)
            self.connected_host += 1
            socket_thread = threading.Thread(target=self.rcv_message_from_client, 
                                             args=[client_name, client_socket, client_address])
            socket_thread.daemon = True
            socket_thread.start()


if __name__ == "__main__":
    try:
        server = PyChessServer("192.168.1.184", 9091, 1000)
        server.accept_connections()
    except socket.error as e:
        print("Exiting ...")
    except KeyboardInterrupt:
        print("Exiting ...")