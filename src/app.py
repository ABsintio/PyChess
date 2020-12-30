import tkinter as tk
from table import *
from chessbar import *


class App:
    def __init__(self, color_player):
        self.app = tk.Tk()
        self.app.title("PyChess")
        self.app.geometry("1100x800")
        self.chss = WhiteChessTable(self.app) if color_player == "white" else BlackChessTable(self.app)
        self.chss.build()
        self.side_bar = ChessSideBar(self.app, "Player1", "Player2", color_player)
        self.side_bar.build()
        self.app.mainloop()