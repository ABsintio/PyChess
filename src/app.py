import tkinter as tk
from table import *
from chessbar import *
from client import *


class App:

    client = None

    def __init__(self, color_player):
        self.app = tk.Tk()
        self.app.title("PyChess")
        self.app.geometry("1100x800")
        self.frame_button = tk.Frame(self.app)
        self.frame_button.pack(fill=tk.BOTH, expand=True)
        self.button = tk.Button(self.frame_button, text="Cliccami!!")
        self.button.bind('<ButtonRelease-1>', App.callback)
        self.button.pack(fill=tk.BOTH, expand=True)

    def start(self):
        self.app.mainloop()

    @classmethod
    def callback(cls, event):
        if cls.client is None:
            client = PyChessClient("Nome", "192.168.1.51", 9090)
            client.connect_to_server()
            client.start_listen_and_receive()
            cls.client = client


a = App("white")
b = App("black")
t_a = threading.Thread(target=a.start)
t_b = threading.Thread(target=b.start)
t_a.start()
t_b.start()