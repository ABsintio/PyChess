import socket
import threading
import sys
import random
import coloredlogs
import argparse
import yaml
import logging
import logging.config
import pickle


argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("-l", "--logger", help="Path del file di configurazione del logger", required=True)
args = argument_parser.parse_args()
config_log = args.logger

logging.config.dictConfig(yaml.load(open(config_log, mode="r"), Loader=yaml.FullLoader))
logger = logging.getLogger("root")
coloredlogs.install(level="DEBUG", logger=logger)


class VirtualRoom(threading.Thread):

    VIRTUAL_ROOM_ID_SIZE = 25

    def __init__(self, identificativo, client1, client2, server):
        super().__init__()
        self.identificativo = identificativo
        self.white, self.white_socket = client1
        self.black, self.black_socket = client2
        self.room_proprietary = server
        self.accept_black = False 
        self.accept_white = True
    
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

    def accept_white_sendto_black(self):
        msg = self.white_socket[0].recv(4096)
        if msg == b"": return
        msg = pickle.loads(msg)
        sendto_msg = f"Messaggio dal giocatore bianco {self.white}: {msg}"
        print(sendto_msg)
        if not self.black_socket[0]._closed:
            sendto_msg = pickle.dumps(msg)
            self.black_socket[0].send(sendto_msg)
        return 0

    def accept_black_sendto_white(self):
        msg = self.black_socket[0].recv(4096)
        if msg == b"": return
        msg = pickle.loads(msg)
        sendto_msg = f"Messaggio dal giocatore nero {self.black}: {msg}"
        print(sendto_msg)
        if not self.white_socket[0]._closed:
            sendto_msg = pickle.dumps(msg)
            self.white_socket[0].send(sendto_msg)
        return 0

    def rcv_clients_msg(self):
        while True:
            if self.accept_white:
                exit_code = self.accept_white_sendto_black()
                if exit_code is None: return
            if self.accept_black:
                exit_code = self.accept_black_sendto_white()
                if exit_code is None: return
            self.accept_white = not self.accept_white
            self.accept_black = not self.accept_black

    def run(self):
        self.rcv_clients_msg()

    def __str__(self):
        return "VirtualRoom(\n" + "\n".join([f"    {k}:{v}" for k, v in self.__dict__.items()]) + "\n)"


class PyChessServer:

    SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self, ip_address, port, max_connession_refused):
        self.ip_address = ip_address
        self.port = port
        self.max_conn_ref = max_connession_refused
        self.connected_host = 0
        self.connection_pool = dict()
        self.virtual_rooms = dict()
        self.virtual_rooms_id = []
        self.virtual_rooms_per_client = dict()
        self.virtual_rooms_idx = 0
        self.start()
    
    def start(self):
        self.SOCKET.bind((self.ip_address, self.port))
        self.SOCKET.listen(self.max_conn_ref)
        logger.debug(f"[SERVER] Il server è in ascolto su ({self.ip_address}, {self.port})")

    def check_virtual_rooms_state(self):
        off_vr = []
        for k, v in self.virtual_rooms.items():
            if not v.is_alive():
                off_vr.append(k)
        for vr in off_vr: 
            virtual_r = self.virtual_rooms[vr]
            virtual_r.white_socket[0].close()
            virtual_r.black_socket[0].close()
            self.virtual_rooms.pop(vr)

    def accept_connections(self):
        try:
            while True:
                client_socket, client_address = self.SOCKET.accept()
                client_name = client_socket.recv(4096)
                client_name = pickle.loads(client_name, encoding="utf-8")
                logger.debug(f"[SERVER] Si è connesso un nuovo client ({client_address}, {client_name})")
                self.connection_pool[client_name] = (client_socket, client_address)
                self.connected_host += 1
                new_virtual_room = self.dispatch_connection()
                if isinstance(new_virtual_room, VirtualRoom):
                    logger.debug(f"[SERVER] Nuova stanza virtuale creata:\n{new_virtual_room}")
                    new_virtual_room.daemon = True
                    new_virtual_room.start()
                    white_socket = new_virtual_room.white_socket[0].send(pickle.dumps("START_WHITE"))
                    black_socket = new_virtual_room.black_socket[0].send(pickle.dumps("START_BLACK"))
                self.check_virtual_rooms_state()

        except Exception as e:
            print(e)
            self.SOCKET.close() # Chiudo la socket del server
            # disconnetto anche tutte quelle dei client
            for _, client_socket in self.connection_pool.items():
                client_socket[0].shutdown(1)
            # Alcuni client possono essere nella stanza virtuale, allora devo scollegare anche quelli
            for _, vr in self.virtual_rooms.items():
                vr.white_socket[0].close()
                vr.black_socket[0].close()

    def dispatch_connection(self):
        connected_host_list = list(self.connection_pool.keys())
        virtual_room = None
        for idx in range(self.virtual_rooms_idx, self.connected_host):
            if (idx + 1) % 2 == 0 and idx > 0:
                client_name1, client_name2 = connected_host_list[idx - 1 - self.virtual_rooms_idx:idx + 1 - self.virtual_rooms_idx]
                client_socket1 = self.connection_pool[client_name1]
                client_socket2 = self.connection_pool[client_name2]
                self.connection_pool.pop(client_name1)
                self.connection_pool.pop(client_name2)
                virtual_room_id = VirtualRoom.generate_random_id(
                    VirtualRoom.VIRTUAL_ROOM_ID_SIZE, self.virtual_rooms_id
                )
                self.virtual_rooms_id.append(virtual_room_id)
                virtual_room = VirtualRoom(
                    virtual_room_id,
                    (client_name1, client_socket1),
                    (client_name2, client_socket2),
                    self.SOCKET
                )
                self.virtual_rooms[virtual_room_id] = virtual_room
                self.virtual_rooms_per_client[client_name1] = virtual_room_id
                self.virtual_rooms_per_client[client_name2] = virtual_room_id
                self.virtual_rooms_idx += 2

        return virtual_room


if __name__ == "__main__":
    server = PyChessServer('', 9090, 1000)
    server.accept_connections()
