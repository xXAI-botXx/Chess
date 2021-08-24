from enum import Enum

import io_helper as io

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
for line in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
    for row in range(1, 9):
        positions += [f"{line}{row}"]

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
        # move
        if self.field.get_field()[from_pos] != None:
            if self.field.get_field()[from_pos].site == self.turn:
                result = self.field.move(from_pos, to_pos)
            else:
                io.print_with_only_delay("You have to choose one of your Chessmen!", 0, 0)
                return None
        else:
            io.print_with_only_delay("You have to choose one of your Chessmen!", 0, 0)
            return None
        if result:
            # change player for next turn
            self.next_player()

    def run_moves(self, moves:list) -> bool:
        """Runs more than one turn on a Chess field. Returns if the execution worked right."""
        # for every move in the list:
        # move
        #...
        # change player for next turn
        self.next_player()

    def get_moves(self, pos:str):
        moves = self.field.valid_moves(pos)
        io.print_with_only_delay(f"\nThere are following moves:\n{moves}", 0, 0)
        io.confirm(f"\n(Press {io.RED}Enter{io.END} to continue)", cleanup=True, fast=True)

    def is_chess_move(self, move) -> bool:
        if type(move) == tuple:
            if len(move) == 2:
                if move[0][0] in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'] and move[0][1] in ['1', '2', '3', '4', '5', '6', '7', '8'] and \
                   move[1][0] in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'] and move[1][1] in ['1', '2', '3', '4', '5', '6', '7', '8']:
                    return True
                else:
                    return False
            else:
                return False
        elif type(move) == str:
            if len(move.split(" ")) == 2:
                pass
            else:
                return False
        else:
            return False

    def get_field(self):
        return self.field.get_field()

    def get_active_player(self):
        return self.turn

    def next_player(self):
        if self.turn == site.WHITE:
            self.turn = site.BLACK
        else:
            self.turn = site.WHITE
