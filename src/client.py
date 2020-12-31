import socket
import sys
import threading
import pickle


class PyChessClient:
    
    SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, client_name, server_ip, server_port, app):
        self.client_name = client_name
        self.server_ip = server_ip
        self.server_port = server_port
        self.app = app
    
    def connect_to_server(self):
        try:
            self.SOCKET.connect((self.server_ip, self.server_port))
            msg = pickle.dumps(self.client_name)
            self.SOCKET.send(msg)
        except socket.gaierror as e:
            print(e)
    
    def send_msg(self, msg):
        try:
            if not self.SOCKET._closed:
                self.SOCKET.send(pickle.dumps(msg))
        except Exception:
            pass

    def rcv_msg(self):
        try:
            while True:
                if self.SOCKET._closed: break
                rcv_msg = self.SOCKET.recv(4096)
                rcv_msg = pickle.loads(rcv_msg)
                if not rcv_msg: break
                if rcv_msg == "START_WHITE":
                    self.app.create_white_board()
                elif rcv_msg == "START_BLACK":
                    self.app.create_black_board()
                elif isinstance(rcv_msg, dict):
                    self.app.replace_board_pieces(rcv_msg)
                else:
                    print("\n" + rcv_msg)
                    print(">>> ", end="")
        except Exception as e:
            print(e)
            pass
        finally:
            if not self.SOCKET._closed: self.SOCKET.close()

    def start_listen(self):
        self.t1 = threading.Thread(target=self.rcv_msg)
        self.t1.start()
    
    def start(self):
        self.connect_to_server()
        self.start_listen()

#client = PyChessClient("Player", "192.168.1.51", 9090)
#client.connect_to_server()
#client.start_listen_and_receive()