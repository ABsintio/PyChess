import tkinter as tk
from table import *
from chessbar import *
from client import *
from functools import partial
import threading
import sys


class App:

    client = None

    def __init__(self, player_name):
        self.player_name = player_name
        self.board = None
        self.app = tk.Tk()
        self.app.title("PyChess")
        self.app.geometry("1100x800")
        self.create_button()

    def start(self):
        self.app.mainloop()

    def create_button(self):
        self.frame_button = tk.Frame(self.app)
        self.frame_button.pack(fill=tk.BOTH, expand=True)
        self.button = tk.Button(self.frame_button, text="Cliccami!!")
        self.button.bind('<ButtonRelease-1>', partial(App.callback, 
                                                      frame_button=self.frame_button, 
                                                      app=self.app,
                                                      pl_name=self.player_name,
                                                      main_app=self
                                                      )
                        )
        self.button.pack(fill=tk.BOTH, expand=True)

    def create_white_board(self):
        self.frame_button.destroy()
        self.button.destroy()
        self.board = WhiteChessTable(self.app, self.client)
        self.board.build()
    
    def create_black_board(self):
        self.frame_button.destroy()
        self.button.destroy()
        self.board = BlackChessTable(self.app, self.client)
        self.board.build()

    def destroy_board(self):
        self.board.destroy()
        self.create_button()
        self.client = None

    @classmethod
    def callback(cls, event, frame_button, app, pl_name, main_app):
        if cls.client is None:
            client = PyChessClient(pl_name, "192.168.1.51", 9090, main_app)
            t = threading.Thread(target=client.start)
            t.start()
            cls.client = client


a = App(sys.argv[-1])
a.start()