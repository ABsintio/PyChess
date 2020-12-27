import tkinter as tk
from tkinter import CENTER
from PIL import ImageTk, Image
from functools import partial


class ChessTable(tk.Frame):

    COLUMN = 8
    ROW = 8
    PIECES_NAMES = {
        "white_king"   : "K",
        "white_queen"  : "Q",
        "white_tower"  : "T",
        "white_bishop" : "B",
        "white_knight" : "N",
        "white_pawn"   : "",
        "black_king"   : "K",
        "black_queen"  : "Q",
        "black_tower"  : "T",
        "black_bishop" : "B",
        "black_knight" : "N",
        "black_pawn"   : ""
    }
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

    myTurn = False
    hold_piece = None

    def __init__(self, master, color_player):
        super().__init__(master=master)
        self.master = master
        self.color_player = color_player
        self.frame_houses = []
        self.labels_frame = []
        self.positions = dict()
        self.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        
        # definisco un dizionare speculare a PIECES_NAME con la 
        # sola differenza che prenderà solo quelli dello stesso
        # colore del giocatore.
        self.alg_name = {v:k for k, v in self.PIECES_NAMES.items() if self.color_player in k}
        self.build()

    def build(self):
        self.create_grid()
        self.place_pieces()
        self.create_event_frame()
    
    def tuple2algebric(self, x, y, piece_name):
        piece_name = self.PIECES_NAMES[piece_name] 
        alpha_pos = chr(97 + x)
        return f"{piece_name}{alpha_pos}{y + 1}"

    def algebric2tuple(self, alg_pos):
        piece_name = self.alg_name[alg_pos[0]]
        x_pos = ord(alg_pos[1]) - 97
        y_pos = int(alg_pos[2]) - 1
        return (piece_name, x_pos, y_pos)
    
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

    @classmethod
    def highlight_label_callback(cls, event, frame, lbls, piece):
        cln = frame.grid_info()['column']
        row = frame.grid_info()['row']
        label_wdg = event.widget
        color = "white" if (cln + row) % 2 == 0 else "gray49"
        if label_wdg.config()['background'][-1] == color:
            color = "lemon chiffon"
        label_wdg.config(bg=color)
        for lbl, x, y in lbls:
            if lbl.config()['background'][-1] == "lemon chiffon" and lbl != label_wdg:
                lbl_color = "white" if (x + y) % 2 == 0 else "gray49"
                lbl.config(bg=lbl_color)
        cls.hold_piece = (label_wdg, piece, cln, row)
        if color in ['white', 'gray49']: cls.hold_piece = None
        
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
                    piece_label.pack()
                    self.positions[piece] = self.tuple2algebric(
                        location_x, location_y, 
                        piece
                    )
                    self.labels_frame.append((piece_label, location_x, location_y))
                    if self.color_player in piece:
                        piece_label.bind(
                            '<ButtonRelease-1>', 
                            partial(ChessTable.highlight_label_callback, 
                                    frame=frame, 
                                    lbls=self.labels_frame,
                                    piece=piece)
                        )

    def create_event_frame(self):
        # TODO
        pass



app = tk.Tk()
app.title("PyChess")
chess_table = ChessTable(app, "black")
#frame2 = tk.Frame(master=app, bg="blue", width=100, height=100)
#frame2.pack(fill=tk.BOTH, side=tk.LEFT)
app.resizable(False, False)
app.mainloop()