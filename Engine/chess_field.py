from enum import Enum

import io_helper as io
import Engine.chess_men as chess
from Engine.chess_engine import lines, modes, positions, site, chessmen

class Field(object):
    def __init__(self, field=dict(), moves=[], new_game=True, mode=modes.CLASSIC):
        self.field = field
        self.moves = moves
        self.mode = mode

        self.graveyard_white = []
        self.graveyard_black = []

        if new_game:
            self.create_new_field()

    def create_new_field(self):
        if self.mode == modes.CLASSIC:
            for pos in positions:
                if pos[1] == '2':
                    self.field[pos] = chess.Pawn(site.WHITE, False, True)
                elif pos[1] == '1':
                    if pos[0] == 'a' or pos[0] == 'h':
                        self.field[pos] = chess.Rook(site.WHITE)
                    elif pos[0] == 'b' or pos[0] == 'g':
                        self.field[pos] = chess.Knight(site.WHITE)
                    elif pos[0] == 'c' or pos[0] == 'f':
                        self.field[pos] = chess.Bishop(site.WHITE)
                    elif pos[0] == 'd':
                        self.field[pos] = chess.King(site.WHITE)
                    elif pos[0] == 'e':
                        self.field[pos] = chess.Queen(site.WHITE)
                elif pos[1] == '7':
                    self.field[pos] = chess.Pawn(site.BLACK, False, True)
                elif pos[1] == '8':
                    if pos[0] == 'a' or pos[0] == 'h':
                        self.field[pos] = chess.Rook(site.BLACK)
                    elif pos[0] == 'b' or pos[0] == 'g':
                        self.field[pos] = chess.Knight(site.BLACK)
                    elif pos[0] == 'c' or pos[0] == 'f':
                        self.field[pos] = chess.Bishop(site.BLACK)
                    elif pos[0] == 'd':
                        self.field[pos] = chess.King(site.BLACK)
                    elif pos[0] == 'e':
                        self.field[pos] = chess.Queen(site.BLACK)
                else:
                    self.field[pos] = None

    def move(self, from_pos, to_pos):
        if to_pos in self.valid_moves(from_pos):
            if self.field[to_pos] != None:
                self.field[from_pos].add_kill(self.field[to_pos].get_name())
                if self.field[to_pos].site == site.WHITE:
                    self.graveyard_white += [self.field[to_pos]]
                    io.print_with_only_delay(f"\nWhite {self.field[from_pos].get_name()} defeats black {self.field[to_pos].get_name()}", 0, 0)
                else:
                    self.graveyard_black += [self.field[to_pos]]
                    io.print_with_only_delay(f"\nBlack {self.field[from_pos].get_name()} defeats white {self.field[to_pos].get_name()}", 0, 0)
                    
                if self.field[from_pos].get_kills() == 3:
                    io.print_with_only_delay(f"\n{self.field[from_pos].get_name()} is heroic.", 0, 0)
                elif self.field[from_pos].get_kills() == 4:
                    io.print_with_only_delay(f"\n{self.field[from_pos].get_name()} will kill'em all.", 0, 0)
                elif self.field[from_pos].get_kills() == 5:
                    io.print_with_only_delay(f"\n{self.field[from_pos].get_name()} is unstoppable.", 0, 0)
                elif self.field[from_pos].get_kills() == 6:
                    io.print_with_only_delay(f"\n{self.field[from_pos].get_name()} is a legend!", 0, 0)

            self.field[to_pos] = self.field[from_pos]
            self.field[from_pos] = None
            # post attack
            if self.field[to_pos].chessman == chessmen.PAWN:
                self.field[to_pos].post_attack(to_pos)
            return True
        else:
            return False

    def valid_moves(self, pos) -> list:    # the new pos have to be in move-set or in attack-set -> but there have to be a enemy
        if self.field[pos] == None:
            return []
        else:
            valid_moves = []
            moves = self.field[pos].get_move_positions()
            for x, y, endless in moves:
                if endless:
                    while True:
                        new_x = self.numerical_field_to_alphabetic(lines[pos[0]]+x)
                        if new_x != None:
                            new_pos = f"{new_x}{int(pos[1])+y}"
                            # position in field
                            if new_pos in positions:
                                # field is free
                                if self.field[new_pos] == None:
                                    # if not added in possible moves
                                    if new_pos not in valid_moves:
                                        valid_moves += [new_pos]
                                else:
                                    break
                            else:
                                break
                else:
                    new_x = self.numerical_field_to_alphabetic(lines[pos[0]]+x)
                    if new_x != None:
                        new_pos = f"{new_x}{int(pos[1])+y}"
                        # position in field
                        if new_pos in positions:
                            # field is free
                            if self.field[new_pos] == None:
                                # if not added in possible moves
                                if new_pos not in valid_moves:
                                    valid_moves += [new_pos]

            attacks = self.field[pos].get_attack_positions()
            for x, y, endless in attacks:
                if endless:
                    while True:
                        new_x = self.numerical_field_to_alphabetic(lines[pos[0]]+x)
                        if new_x != None:
                            new_pos = f"{new_x}{int(pos[1])+y}"
                            # position in field
                            if new_pos in positions:
                                # field is enemy
                                if self.field[new_pos] != None and self.field[new_pos].site != self.field[pos].site:
                                    # if not added in possible moves
                                    if new_pos not in valid_moves:
                                        valid_moves += [new_pos]
                                else:
                                    break
                            else:
                                break
                else:
                    new_x = self.numerical_field_to_alphabetic(lines[pos[0]]+x)
                    if new_x != None:
                        new_pos = f"{new_x}{int(pos[1])+y}"
                        # position in field
                        if new_pos in positions:
                            # field is enemy
                            if self.field[new_pos] != None and self.field[new_pos].site != self.field[pos].site:
                                # if not added in possible moves
                                if new_pos not in valid_moves:
                                    valid_moves += [new_pos]

            return valid_moves

    def numerical_field_to_alphabetic(self, num:int):
        try:
            return {1:'a', 2:'b', 3:'c', 4:'d', 5:'e', 6:'f', 7:'g', 8:'h'}[num]
        except KeyError:
            return None

    def get_field(self) -> dict:
        return self.field
