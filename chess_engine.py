from enum import Enum

from chess_field import Field

# Chess Pieces:
#   Pawn = Bauer
#   Rook = Turm
#   Knight = Pferd
#   Bishop = Ritter
#   Queen = Königin
#   King = König
chessmen = Enum("chessmen", "PAWN ROOK KNIGHT BISHOP QUEEN KING")
site = Enum("site", "WHITE BLACK")
modes = Enum("modes", "CLASSIC")
lines = {'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7, 'h':8}
positions = set()
for lines in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
    for rows in range(1, 9):
        positions.add(f"{lines}{rows}")

class Engine(object):
    def __init__(self, new_game:bool, mode=modes.CLASSIC):
        if new_game:
            self.field = Field(new_game=True, mode=mode)
        else:
            self.load_game()

    def save_game(self):
        pass

    def load_game(self):
        pass
        # 1. get path to save txt -> while its a right path or cancel

    def run_move(self, move:str):
        pass

    def run_moves(self, moves:list):
        pass

    def is_chess_move(self, move:str) -> bool:
        pass
