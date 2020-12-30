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
    PIECES_XY_DICT_WHITE = {
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
    PIECES_XY_DICT_BLACK = {
        "black_king"   : [(4, 7)],
        "black_queen"  : [(3, 7)],
        "black_tower"  : [(0, 7), (7, 7)],
        "black_bishop" : [(2, 7), (5, 7)],
        "black_knight" : [(1, 7), (6, 7)],
        "black_pawn"   : [(x, 6) for x in range(8)],
        "white_king"   : [(4, 0)],
        "white_queen"  : [(3, 0)],
        "white_tower"  : [(0, 0), (7, 0)],
        "white_bishop" : [(2, 0), (5, 0)],
        "white_knight" : [(1, 0), (6, 0)],
        "white_pawn"   : [(x, 1) for x in range(8)]
    }
    PIECES_IMG_DICT = {
        "white_king"   : "pieces/white_king.png",
        "white_queen"  : "pieces/white_queen.png",
        "white_tower"  : "pieces/white_tower.png",
        "white_bishop" : "pieces/white_bishop.png",
        "white_knight" : "pieces/white_knight.png",
        "white_pawn"   : "pieces/white_pawn.png",
        "black_king"   : "pieces/black_king.png",
        "black_queen"  : "pieces/black_queen.png",
        "black_tower"  : "pieces/black_tower.png",
        "black_bishop" : "pieces/black_bishop.png",
        "black_knight" : "pieces/black_knight.png",
        "black_pawn"   : "pieces/black_pawn.png"
    }

    myTurn = False
    hold_piece = ()

    def __init__(self, master, client):
        super().__init__(master=master)
        self.master = master
        self.frame_houses = []
        self.positions = dict()
        self.labels_frame = []
        self.coords = [y for x in self.PIECES_XY_DICT_WHITE.values() for y in x]
        #self.config(width=800)
        #self.config(height=800)
        self.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        self.client = client

    @staticmethod
    def tuple2algebric(x, y, piece_name):
        piece_name = ChessTable.PIECES_NAMES[piece_name] 
        alpha_pos = chr(97 + x)
        return f"{piece_name}{alpha_pos}{y + 1}"
    
    @staticmethod
    def algebric2tuple(alg_pos, alg_name):
        piece_name = alg_name[alg_pos[0]] if len(alg_pos) == 3 else alg_name[""]
        x_pos = ord(alg_pos[1]) - 97 if len(alg_pos) == 3 else ord(alg_pos[0]) - 97
        y_pos = int(alg_pos[2]) - 1 if len(alg_pos) == 3 else int(alg_pos[1]) - 1
        return (piece_name, x_pos, y_pos)

    @staticmethod
    def get_position_from_labels(lable, lables):
        for lbl in lables:
            if lbl[0] == lable: return lbl

    @staticmethod
    def get_frame_from_position(x, y, frame_houses):
        return list(filter(lambda q: q.grid_info()['column'] == x and q.grid_info()['row'] == y, frame_houses))[-1]

    @classmethod
    def highlight_label_callback(cls, event, frame, lbls, piece, piece_pos_name):
        cln = frame.grid_info()['column']
        row = frame.grid_info()['row']
        label_wdg = event.widget
        color = "white" if (cln + row) % 2 == 0 else "gray49"
        if label_wdg.config()['background'][-1] == color:
            color = "lemon chiffon"
        label_wdg.config(bg=color)
        for lbl, _, x, y in lbls:
            if lbl.config()['background'][-1] == "lemon chiffon" and lbl != label_wdg:
                lbl_color = "white" if (x + y) % 2 == 0 else "gray49"
                lbl.config(bg=lbl_color)
        cls.hold_piece = (label_wdg, frame, piece, piece_pos_name, cln, row)
        if color in ['white', 'gray49']: cls.hold_piece = ()

    @classmethod
    def move_piece_callback(cls, event, lables, frames_houses, positions, alg_names, client):
        if cls.hold_piece != ():
            lbl, frame, piece, piece_pos_name, cln, row = cls.hold_piece
            frame_to_color = 'white' if (cln + row) % 2 == 0 else "grey49"
            if isinstance(event.widget, tk.Frame):
                c = event.widget.grid_info()['column']
                r = event.widget.grid_info()['row']
            else:
                lbl_to, piece_to, pos_x, pos_y = cls.get_position_from_labels(event.widget, lables)
                c = pos_x
                r = pos_y
            
            frame_from_color = 'white' if (c + r) % 2 == 0 else "grey49"
            frame_to = cls.get_frame_from_position(pos_x, pos_y, frames_houses) if isinstance(event.widget, tk.Label) else event.widget
            if cls.check_move(piece, cln, row, c, r, positions, alg_names) or ("pawn" in piece and cls.isLegal_pawn_diagonal_move(cln, row, c, r, event.widget)):
                if isinstance(event.widget, tk.Label):
                    if "pawn" in piece and not cls.isLegal_pawn_diagonal_move(cln, row, c, r, event.widget): return
                    lbl_to.destroy()
                    lables.remove((lbl_to, piece_to, pos_x, pos_y))
                    piece_to_name = ""
                    for k, v in positions.items():
                        if v == cls.tuple2algebric(c, r, piece_to):
                            piece_to_name = k
                            break
                    positions.pop(piece_to_name)
                frame_to.grid(column=cln,row=row,sticky="nsew")
                frame_to.config(bg=frame_to_color)
                frame.grid(column=c,row=r,sticky="nsew")
                lbl.config(bg=frame_from_color)
                index_of = lables.index((lbl, piece, cln, row))
                lables[index_of] = (lbl, piece, c, r)
                cls.hold_piece = ()
                positions[piece_pos_name] = cls.tuple2algebric(c, r, piece)
                client.send_msg(positions)
                return

    @staticmethod
    def isLegal_pawn_move(x_from, y_from, x_to, y_to, positions=None, alg_name=None):
        return (x_from, y_from - 1) == (x_to, y_to) or \
               (y_from == 6 and ((x_from, y_from - 2) == (x_to, y_to)))

    @staticmethod
    def isLegal_pawn_diagonal_move(x_from, y_from, x_to, y_to, diag_widget):
        return isinstance(diag_widget, tk.Label) and (
            (x_from + 1, y_from - 1) == (x_to, y_to) or \
            (x_from - 1, y_from - 1) == (x_to, y_to)
        )
    
    @staticmethod
    def isLegal_king_move(x_from, y_from, x_to, y_to, positions=None, alg_name=None):
        return (x_from, y_from - 1) == (x_to, y_to) or \
               (x_from + 1, y_from - 1) == (x_to, y_to) or \
               (x_from - 1, y_from - 1) == (x_to, y_to) or \
               (x_from - 1, y_from) == (x_to, y_to) or \
               (x_from - 1, y_from + 1) == (x_to, y_to) or \
               (x_from, y_from + 1) == (x_to, y_to) or \
               (x_from + 1, y_from + 1) == (x_to, y_to) or \
               (x_from + 1, y_from) == (x_to, y_to)
    
    @staticmethod
    def isLegal_knight_move(x_from, y_from, x_to, y_to, positions=None, alg_name=None):
        return (x_from - 1, y_from - 2) == (x_to, y_to) or \
               (x_from + 1, y_from - 2) == (x_to, y_to) or \
               (x_from + 2, y_from - 1) == (x_to, y_to) or \
               (x_from + 2, y_from + 1) == (x_to, y_to) or \
               (x_from + 1, y_from + 2) == (x_to, y_to) or \
               (x_from - 1, y_from + 2) == (x_to, y_to) or \
               (x_from - 2, y_from + 1) == (x_to, y_to) or \
               (x_from - 2, y_from - 1) == (x_to, y_to)
    
    @staticmethod
    def isLegal_tower_move(x_from, y_from, x_to, y_to, positions, alg_name):
        other_piece_positions = [ChessTable.algebric2tuple(x, alg_name) for x in positions.values()]
        current_trajectory = []
        trajectory_up = [(x_from, y_from - j) for j in range(0, y_from + 1)]
        trajectory_down = [(x_from, y_from + j) for j in range(0, 8 - y_from)]
        trajectory_rigth = [(x_from + i, y_from) for i in range(0, 8 - x_from)]
        trajectory_left = [(x_from - i, y_from) for i in range(0, x_from + 1)]
        if (x_to, y_to) in trajectory_up: current_trajectory = trajectory_up
        elif (x_to, y_to) in trajectory_down: current_trajectory = trajectory_down
        elif (x_to, y_to) in trajectory_rigth: current_trajectory = trajectory_rigth
        elif (x_to, y_to) in trajectory_left: current_trajectory = trajectory_left
        else:
            return False

        for oth_pos in other_piece_positions:
            _, pos_x, pos_y = oth_pos
            if (pos_x, pos_y) in current_trajectory:
                from_pos = current_trajectory.index((x_from, y_from))
                pos = current_trajectory.index((pos_x, pos_y))
                to_pos = current_trajectory.index((x_to, y_to))
                if from_pos < pos < to_pos: 
                    return False
        return True
    
    @staticmethod
    def isLegal_bishop_move(x_from, y_from, x_to, y_to, positions, alg_name):
        other_piece_positions = [ChessTable.algebric2tuple(x, alg_name) for x in positions.values()]
        delta_xprime_a = abs(0 - x_from) + 1
        delta_yprime_a = abs(8 - y_from)
        delta_xsecond_a = abs(x_from - 8)
        delta_ysecond_a = abs(y_from - 0) + 1
        range_Mno = range(1, min(delta_xprime_a, delta_ysecond_a))
        range_Mso = range(1, min(delta_xprime_a, delta_yprime_a))
        range_Mne = range(1, min(delta_xsecond_a, delta_ysecond_a))
        range_Mse = range(1, min(delta_xsecond_a, delta_yprime_a))
        trajectory_Mno = [(x_from - i, y_from - i) for i in range_Mno]
        trajectory_Mso = [(x_from - i, y_from + i) for i in range_Mso]
        trajectory_Mne = [(x_from + i, y_from - i) for i in range_Mne]
        trajectory_Mse = [(x_from + i, y_from + i) for i in range_Mse]
        current_trajectory = []
        if (x_to, y_to) in trajectory_Mno: current_trajectory = trajectory_Mno
        elif (x_to, y_to) in trajectory_Mso: current_trajectory = trajectory_Mso
        elif (x_to, y_to) in trajectory_Mne: current_trajectory = trajectory_Mne
        elif (x_to, y_to) in trajectory_Mse: current_trajectory = trajectory_Mse
        else:
            return False
        for oth_pos in other_piece_positions:
            _, pos_x, pos_y = oth_pos
            if (pos_x, pos_y) in current_trajectory:
                pos = current_trajectory.index((pos_x, pos_y))
                to_pos = current_trajectory.index((x_to, y_to))
                if pos < to_pos: 
                    return False
        return True

    @staticmethod
    def isLegal_queen_move(x_from, y_from, x_to, y_to, positions, alg_name):
        return ChessTable.isLegal_tower_move(x_from, y_from, x_to, y_to, positions, alg_name) or \
               ChessTable.isLegal_bishop_move(x_from, y_from, x_to, y_to, positions, alg_name)

    @staticmethod
    def check_move(piece, x_from, y_from, x_to, y_to, positions, alg_name):
        piece_check_functions = {
            "white_king"   : ChessTable.isLegal_king_move,
            "white_queen"  : ChessTable.isLegal_queen_move,
            "white_tower"  : ChessTable.isLegal_tower_move,
            "white_bishop" : ChessTable.isLegal_bishop_move,
            "white_knight" : ChessTable.isLegal_knight_move,
            "white_pawn"   : ChessTable.isLegal_pawn_move,
            "black_king"   : ChessTable.isLegal_king_move,
            "black_queen"  : ChessTable.isLegal_queen_move,
            "black_tower"  : ChessTable.isLegal_tower_move,
            "black_bishop" : ChessTable.isLegal_bishop_move,
            "black_knight" : ChessTable.isLegal_knight_move,
            "black_pawn"   : ChessTable.isLegal_pawn_move
        }
        return piece_check_functions[piece](x_from, y_from, x_to, y_to, positions, alg_name)


class WhiteChessTable(ChessTable):

    def __init__(self, master, client):
        super().__init__(master=master, client=client)
        self.color_player = "white"
        self.piece_xy_pos = self.PIECES_XY_DICT_WHITE
        self.alg_name = {v:k for k, v in self.PIECES_NAMES.items() if self.color_player in k}

    def build(self):
        self.create_grid()
        self.place_pieces()
        self.create_event_frame()
    
    def create_grid(self):
        cartesian_product = [(x, y) for x in range(self.COLUMN) for y in range(self.ROW)]
        index = 0
        for c, r in cartesian_product:
            if c == 7: index += 1
            w, h = (100, 100)
            frame = tk.Frame(
                master=self,
                relief=tk.RAISED,
                width=w, height=h,
                bg="gray49" if (c + r) % 2 != 0 else "white",
                bd=1
            )
            frame.grid(column=c,row=r,sticky="nsew")
            frame.pack_propagate(0)
            self.frame_houses.append(frame)
        
    def place_pieces(self):
        occurrence_piece = {k:0 for k in self.PIECES_NAMES.keys()}
        for frame in self.frame_houses:
            location_x = frame.grid_info()['column']
            location_y = frame.grid_info()['row']
            for piece, img_name in self.PIECES_IMG_DICT.items():
                if (location_x, location_y) in self.piece_xy_pos[piece]:
                    occ = occurrence_piece[piece]
                    img_obj = Image.open(img_name)
                    img = ImageTk.PhotoImage(image=img_obj)
                    piece_label = tk.Label(
                        master=frame,
                        bg=frame.config()['background'][-1],
                        image=img,
                        width=100,
                        height=100
                    )
                    piece_label.image = img
                    piece_label.pack(fill=tk.BOTH, expand=False)
                    self.positions[f"{piece}_{occ}"] = self.tuple2algebric(
                        location_x, location_y, 
                        piece
                    )
                    occurrence_piece[piece] += 1
                    self.labels_frame.append((piece_label, piece, location_x, location_y))
                    if self.color_player in piece:
                        piece_label.bind(
                            '<ButtonRelease-1>', 
                            partial(ChessTable.highlight_label_callback, 
                                    frame=frame, 
                                    lbls=self.labels_frame,
                                    piece=piece,
                                    piece_pos_name=f"{piece}_{occ}"
                                )
                        )
                    else:
                        piece_label.bind('<ButtonRelease-1>', partial(
                            ChessTable.move_piece_callback,
                            lables=self.labels_frame,
                            frames_houses=self.frame_houses,
                            positions=self.positions,
                            alg_names=self.alg_name,
                            client=self.client
                            ))

    def create_event_frame(self):
        for frame in self.frame_houses:
            # Bindig of an event to each frame
            frame.bind("<ButtonRelease-1>", partial(
                ChessTable.move_piece_callback,
                lables=self.labels_frame,
                frames_houses=self.frame_houses,
                positions=self.positions,
                alg_names=self.alg_name,
                client=self.client
                ))


class BlackChessTable(WhiteChessTable):
    def __init__(self, master, client):
        super().__init__(master=master, client=client)
        self.piece_xy_pos = self.PIECES_XY_DICT_BLACK
        self.color_player = "black"
