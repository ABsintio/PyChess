import socket
import sys


class PyChessClient:
    
    SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, client_name, server_ip, server_port):
        self.client_name = client_name
        self.server_ip = server_ip
        self.server_port = server_port
    
    def connect_to_server(self):
        try:
            self.SOCKET.connect((self.server_ip, self.server_port))
            self.SOCKET.send(self.client_name.encode("utf-8"))
        except socket.gaierror as e:
            print(e)
    
    def send_msg(self):
        while (msg := input(">>> ") != "quit"):
            self.SOCKET.send(msg.encode("utf-8"))
        self.SOCKET.close()

client = PyChessClient(sys.argv[1], "192.168.1.184", 9091)
client.connect_to_server()
client.send_msg()