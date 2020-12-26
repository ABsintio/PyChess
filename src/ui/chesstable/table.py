import tkinter as tk
from tkinter import CENTER
from PIL import ImageTk, Image


class ChessTable(tk.Tk):

    COLUMN = 8
    ROW = 8
    PIECES_XY_DICT = {
        "white_king"   : [(4, 7)],
        "white_queen"  : [(3, 7)],
        "white_tower"  : [(0, 7), (7, 7)],
        "white_bishop" : [(2, 7), (5, 7)],
        "white_knight" : [(1, 7), (6, 7)],
        "white_pawn"   : [(x, 6) for x in range(8)],
        "black_king"   : [(4, 0)],
        "black_queen"  : [(3, 0)],
        "black_tower"  : [(0, 0), (7, 0)],
        "black_bishop" : [(2, 0), (5, 0)],
        "black_knight" : [(1, 0), (6, 0)],
        "black_pawn"   : [(x, 1) for x in range(8)]
    }
    PIECES_IMG_DICT = {
        "white_king"   : "../pieces/white_king.png",
        "white_queen"  : "../pieces/white_queen.png",
        "white_tower"  : "../pieces/white_tower.png",
        "white_bishop" : "../pieces/white_bishop.png",
        "white_knight" : "../pieces/white_knight.png",
        "white_pawn"   : "../pieces/white_pawn.png",
        "black_king"   : "../pieces/black_king.png",
        "black_queen"  : "../pieces/black_queen.png",
        "black_tower"  : "../pieces/black_tower.png",
        "black_bishop" : "../pieces/black_bishop.png",
        "black_knight" : "../pieces/black_knight.png",
        "black_pawn"   : "../pieces/black_pawn.png"
    }

    def __init__(self):
        super().__init__()
        self.frame_houses = []
        self.build()
        self.title = "PyChess"

    def build(self):
        self.create_grid()
        self.place_pieces()
    
    def create_grid(self):
        cartesian_product = [(x, y) for x in range(self.COLUMN) for y in range(self.ROW)]
        index = 0
        for c, r in cartesian_product:
            self.columnconfigure(index, weight=1, minsize=100)
            self.rowconfigure(index, weight=1, minsize=100)
            if c == 7: index += 1
            frame = tk.Frame(
                master=self,
                relief=tk.RAISED,
                bg="gray49" if (c + r) % 2 != 0 else "white",
            )
            frame.grid(column=c,row=r,sticky="nsew")
            self.frame_houses.append(frame)
        
    def place_pieces(self):
        for frame in self.frame_houses:
            location_x = frame.grid_info()['column']
            location_y = frame.grid_info()['row']
            for piece, img_name in self.PIECES_IMG_DICT.items():
                if (location_x, location_y) in self.PIECES_XY_DICT[piece]:
                    frame.update()
                    img_obj = Image.open(img_name)
                    img = ImageTk.PhotoImage(image=img_obj.resize((100, 100)))
                    piece_label = tk.Label(
                        master=frame,
                        bg=frame.config()['background'][-1],
                        image=img)
                    piece_label.image = img
                    piece_label.pack(fill=tk.BOTH)


chess_table = ChessTable()
chess_table.mainloop()