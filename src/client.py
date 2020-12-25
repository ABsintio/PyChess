import socket
import sys
import threading


class PyChessClient:
    
    SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, client_name, server_ip, server_port):
        self.client_name = client_name
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket_closed = False
    
    def connect_to_server(self):
        try:
            self.SOCKET.connect((self.server_ip, self.server_port))
            self.SOCKET.send(self.client_name.encode("utf-8"))
        except socket.gaierror as e:
            print(e)
    
    def send_msg(self):
        while True:
            msg = input(">>> ")
            if msg == "quit":
                break
            self.SOCKET.send(msg.encode("utf-8"))
        self.SOCKET.close()
        self.socket_closed = True

    def rcv_msg(self):
        while True:
            try:
                rcv_msg = self.SOCKET.recv(4096).decode("utf-8")
                print(rcv_msg)
            except OSError:
                return

    def start_listen_and_receive(self):
        t1 = threading.Thread(target=self.send_msg)
        t2 = threading.Thread(target=self.rcv_msg)
        t1.start()
        t2.start()
    

client = PyChessClient(sys.argv[1], "192.168.1.184", 9091)
client.connect_to_server()
client.start_listen_and_receive()