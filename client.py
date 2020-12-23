import socket
import sys

host = "192.168.1.51"
port = 9091

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sock.connect((host, port))
    while True:
        msg = input(">>> ")
        if msg == "quit":
            sock.close()
            sys.exit(0)
        else:
            sock.send(msg.encode("utf-8"))
except Exception as e:
    print(e)