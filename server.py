import socket
import threading
import sys


class PyChessServer:

    SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    CONNECTED_HOST = 0

    def __init__(self, ip_address, port, max_connession_refused):
        self.ip_address = ip_address
        self.port = port
        self.max_conn_ref = max_connession_refused
        self.start()
    
    def start(self):
        self.SOCKET.bind((self.ip_address, self.port))
        self.SOCKET.listen(self.max_conn_ref)

    def rcv_message_from_client(self, connection_obj, client_address):
        while (msg := connection_obj.recv(4096).decode("utf-8")):
            print(f"Messaggio da {client_address} -> {msg}")
        self.CONNECTED_HOST -= 1

    def accept_connections(self):
        while True:
            client_socket, client_address = self.SOCKET.accept()
            self.CONNECTED_HOST += 1
            socket_thread = threading.Thread(target=self.rcv_message_from_client, args=[client_socket, client_address])
            socket_thread.daemon = True
            socket_thread.start()
            socket_thread.join()
            if not socket_thread.is_alive() and self.CONNECTED_HOST == 0:
                print("Chiusura della socket ... ")
                self.SOCKET.close()
                sys.exit(0)


if __name__ == "__main__":
    server = PyChessServer("192.168.1.51", 9091, 1000)
    server.accept_connections()