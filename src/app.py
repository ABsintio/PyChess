import tkinter as tk
from table import *
from chessbar import *
from client import *
from functools import partial
import threading


class App:

    client = None

    def __init__(self, color_player):
        self.app = tk.Tk()
        self.app.title("PyChess")
        self.app.geometry("1100x800")
        self.frame_button = tk.Frame(self.app)
        self.frame_button.pack(fill=tk.BOTH, expand=True)
        self.button = tk.Button(self.frame_button, text="Cliccami!!")
        self.button.bind('<ButtonRelease-1>', partial(App.callback, frame_button=self.frame_button, app=self.app))
        self.button.pack(fill=tk.BOTH, expand=True)

    def start(self):
        self.app.mainloop()

    @classmethod
    def callback(cls, event, frame_button, app):
        if cls.client is None:
            client = PyChessClient("Nome1", "192.168.1.51", 9090)
            t = threading.Thread(target=client.start)
            t.start()
            cls.client = client
            frame_button.destroy()
            white_board = WhiteChessTable(app)
            white_board.build()


a = App("white")
a.start()