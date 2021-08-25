from enum import Enum
import random

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
            self.gameover = False
        else:
            self.load_game()

    def save_game(self):
        pass

    def load_game(self):
        pass
        # 1. get path to save txt -> while its a right path or cancel

    def run_move(self, from_pos:str, to_pos:str) -> tuple:    
        """Runs a turn on a Chess field. Returns if the execution worked right and output from the game."""
        messages = ""
        result = False
        # move
        if not self.gameover:
            if self.field.get_field()[from_pos] != None:
                if self.field.get_field()[from_pos].site == self.turn:
                    turn_result = self.field.move(self.field.field, from_pos, to_pos)
                    result = turn_result[0]
                    messages += turn_result[1]
                    # check safety of the enemy
                    if self.field.is_check_mate(self.field.field, self.field.get_opposite_site(self.turn)):
                        self.gameover = True
                        self.winner = self.turn
                        if self.winner == site.WHITE:
                            messages += "\n\nBLACK is in checkmate!"
                            messages += "\nWHITE won this game!"
                        else:
                            messages += "\n\WHITE is in checkmate!"
                            messages += "\nBLACK won this game!"
                    elif self.field.is_check(self.field.field, self.field.get_opposite_site(self.turn)):
                        if self.field.get_opposite_site(self.turn) == site.WHITE:
                            messages += "\nWHITE is in check!"
                        else:
                            messages += "BLACK is in check!"
                else:
                    messages += "\nYou have to choose one of your Chessmen!"
            else:
                messages += "You have to choose one of your Chessmen!"
            if result:
                # change player for next turn
                self.next_player()
        else:
            messages += "The Game is over!"

        return (result, messages)

    def run_random_move(self, my_site:str) -> tuple:
        # get all positions
        my_chessmen = []
        for pos in positions:
            if self.field.field[pos].site == site.WHITE and my_site == "WHITE":
                my_chessmen += [self.field.field[pos]]
            elif self.field.field[pos].site == site.BLACK and my_site == "BLACK":
                my_chessmen += [self.field.field[pos]]
        # all moves
        all_moves = []
        for my_chessman in my_chessmen:
            for pos in self.field.valid_moves(my_chessman):
                all_moves += [(my_chessman, pos)]
        # choose a random move
        if my_site == "WHITE":
            my_site = site.WHITE
        else:
            my_site = site.BLACK
        move = random.choice(all_moves)
        while self.field.is_check(self.field.move_without_changes(self.field.field, move[0], move[1]), my_site):
            move = random.choice(all_moves)
        return move

    def run_moves(self, moves:list) -> bool:
        """Runs more than one turn on a Chess field. Returns if the execution worked right."""
        # for every move in the list:
        # move
        #...
        # change player for next turn
        self.next_player()

    def get_moves(self, pos:str):
        moves = self.field.valid_moves(pos)
        return f"\nThere are following moves:\n{moves}"

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
