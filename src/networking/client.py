import socket
import sys
import threading
import pickle


class PyChessClient:
    
    SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, client_name, server_ip, server_port):
        self.client_name = client_name
        self.server_ip = server_ip
        self.server_port = server_port
    
    def connect_to_server(self):
        try:
            self.SOCKET.connect((self.server_ip, self.server_port))
            msg = pickle.dumps(self.client_name)
            self.SOCKET.send(msg)
        except socket.gaierror as e:
            print(e)
    
    def send_msg(self):
        try:
            while True:
                if self.SOCKET._closed: break
                msg = input(">>> ")
                msg = pickle.dumps(msg)
                if msg == "quit" or not msg: break
                self.SOCKET.send(msg)
        except Exception as e:
            print(e)
        finally:
            if not self.SOCKET._closed: self.SOCKET.close()

    def rcv_msg(self):
        try:
            while True:
                #print("Ciao")
                if self.SOCKET._closed: break
                rcv_msg = self.SOCKET.recv(4096)
                rcv_msg = pickle.loads(rcv_msg)
                if not rcv_msg: break
                print("\n" + rcv_msg)
                print(">>> ", end="")
        except Exception:
            pass
        finally:
            if not self.SOCKET._closed: self.SOCKET.close()

    def start_listen_and_receive(self):
        self.t1 = threading.Thread(target=self.send_msg)
        self.t2 = threading.Thread(target=self.rcv_msg)
        self.t1.start()
        self.t2.start()
        self.t1.join()
        self.t2.join()

client = PyChessClient(sys.argv[1], "192.168.1.184", 9090)
client.connect_to_server()
client.start_listen_and_receive()