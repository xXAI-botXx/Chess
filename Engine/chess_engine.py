from enum import Enum

# Chess Pieces:
#   Pawn = Bauer (kein Zeichen oder hier: P)
#   Rook = Turm (R)
#   Knight = Pferd (N)
#   Bishop = Läufer (B)
#   Queen = Dame (Q)
#   King = König (K)
chessmen = Enum("chessmen", "PAWN ROOK KNIGHT BISHOP QUEEN KING")
site = Enum("site", "WHITE BLACK")
modes = Enum("modes", "CLASSIC")
lines = {'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7, 'h':8}
positions = list()
for lines in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
    for rows in range(1, 9):
        positions += [f"{lines}{rows}"]

from Engine.chess_field import Field

class Engine(object):
    def __init__(self, new_game:bool, mode=modes.CLASSIC, turn=site.WHITE):
        if new_game:
            self.field = Field(new_game=True, mode=mode)
            self.turn = turn
        else:
            self.load_game()

    def save_game(self):
        pass

    def load_game(self):
        pass
        # 1. get path to save txt -> while its a right path or cancel

    def run_move(self, from_pos:str, to_pos:str) -> bool:    
        """Runs a turn on a Chess field. Returns if the execution worked right."""
        pass

    def run_moves(self, moves:list) -> bool:
        """Runs more than one turn on a Chess field. Returns if the execution worked right."""
        # move
        #...
        # change player for next turn
        self.next_player()

    def is_chess_move(self, move:str) -> bool:
        # for every move in the list:
        # move
        #...
        # change player for next turn
        self.next_player()

    def get_field(self):
        return self.field.get_field()

    def get_active_player(self):
        return self.turn

    def next_player(self):
        if self.turn == site.WHITE:
            self.turn = site.BLACK
        else:
            self.turn = site.WHITE
