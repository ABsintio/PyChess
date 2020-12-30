import tkinter as tk
from tkinter import CENTER


class ChessSideBar(tk.Frame):
    def __init__(self, master, white_name, black_name, color_player):
        super().__init__(master=master)
        self.white_name = white_name
        self.black_name = black_name
        self.color_player = color_player
        self.config(bd=1)
        self.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
    
    def build(self):
        self.place_frames()
        self.place_labels()
        self.place_text()

    def place_frames(self):
        self.white_label_frame = tk.Frame(self, relief=tk.RAISED, bd=2, bg="gray64")
        self.black_label_frame = tk.Frame(self, relief=tk.RAISED, bd=2, bg="gray64")
        self.text_move_frame = tk.Frame(self, relief=tk.RAISED, bd=2, bg="gray64")
        self.white_label_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        self.black_label_frame.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=True)
        self.text_move_frame.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=True)

    def place_labels(self):
        white_label = tk.Label(self.white_label_frame, text=self.black_name, bg="gray64", height=2)
        white_label.pack(fill=tk.BOTH, side=tk.RIGHT, anchor=tk.CENTER)
        black_label = tk.Label(self.black_label_frame, text=self.white_name, bg="gray64", height=2)
        black_label.pack(fill=tk.BOTH, side=tk.RIGHT, anchor=tk.CENTER)

    def place_text(self):
        text = tk.Text(self.text_move_frame, width=50, height=52)
        text.pack(fill=tk.BOTH, anchor=tk.CENTER, expand=True)