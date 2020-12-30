import tkinter as tk
from ui.chesstable.table import WhiteChessTable
from ui.sidebars.chessbar import ChessSideBar

app = tk.Tk()
app.title("PyChess")
#chess_table = WhiteChessTable(app)
#chess_table.build()
chess_table = WhiteChessTable(app)
chess_table.build()
chess_side_bar = ChessSideBar(app, "Player1", "Player2", "white")
chess_side_bar.build()
app.resizable(False, False)
app.mainloop()