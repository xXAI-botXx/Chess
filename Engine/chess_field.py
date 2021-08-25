from copy import deepcopy

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

    def move(self, field, from_pos, to_pos) -> tuple:
        """executes a move (if possible) directly on the field.\n 
           Returns if the turn has been executed"""
        messages = ""
        if to_pos in self.valid_moves(field, from_pos):
            # check if danger the king
            new_field = self.move_without_changes(field, from_pos, to_pos)
            if not self.is_check(new_field, field[from_pos].site):
                if field[to_pos] != None:
                    field[from_pos].add_kill(field[to_pos].get_name())
                    if field[to_pos].site == site.WHITE:
                        self.graveyard_white += [field[to_pos]]
                        messages += f"\nBlack {field[from_pos].get_name()} defeats white {field[to_pos].get_name()}"
                    else:
                        self.graveyard_black += [field[to_pos]]
                        messages += f"\nWhite {field[from_pos].get_name()} defeats black {field[to_pos].get_name()}"
                        
                    if field[from_pos].get_kills() == 3:
                        messages += f"\n{field[from_pos].get_name()} is heroic."
                    elif field[from_pos].get_kills() == 4:
                        messages += f"\n{field[from_pos].get_name()} will kill'em all."
                    elif field[from_pos].get_kills() == 5:
                        messages += f"\n{field[from_pos].get_name()} is unstoppable."
                    elif field[from_pos].get_kills() == 6:
                        messages += f"\n{field[from_pos].get_name()} is a legend!"

                field[to_pos] = field[from_pos]
                field[from_pos] = None
                # post attack
                if field[to_pos].chessman == chessmen.PAWN:
                    field[to_pos].post_attack(to_pos)
                self.moves += [(from_pos, to_pos)]
                return (True, messages)
            else:
                messages += "\nYou have to make the safety of your king sure!"
                return (False, messages)
        else:
            return (False, messages)

    def move_without_changes(self, field, from_pos, to_pos) -> dict:
        """executes a turn on a new map and returns that map"""
        # all objects (the chessmen) have to be copies!!!
        copy_field = deepcopy(field)
        if to_pos in self.valid_moves(field, from_pos):
            if copy_field[to_pos] != None:
                copy_field[from_pos].add_kill(copy_field[to_pos].get_name())
                if copy_field[to_pos].site == site.WHITE:
                    self.graveyard_white += [copy_field[to_pos]]
                else:
                    self.graveyard_black += [copy_field[to_pos]]

            copy_field[to_pos] = copy_field[from_pos]
            copy_field[from_pos] = None
            # post attack
            if copy_field[to_pos].chessman == chessmen.PAWN:
                copy_field[to_pos].post_attack(to_pos)
            self.moves += [(from_pos, to_pos)]
            return copy_field
        else:
            return None

    def valid_moves(self, field, pos) -> list:    # the new pos have to be in move-set or in attack-set -> but there have to be a enemy
        if field[pos] == None:
            return []
        else:
            valid_moves = []
            moves = field[pos].get_move_positions()
            for x, y, endless in moves:
                if endless:
                    new_x = self.numerical_field_to_alphabetic(lines[pos[0]])
                    new_y = int(pos[1])
                    while True:
                        new_x = self.numerical_field_to_alphabetic(lines[new_x]+x)
                        new_y += y
                        if new_x != None:
                            new_pos = f"{new_x}{new_y}"
                            # position in field
                            if new_pos in positions:
                                # field is free
                                if field[new_pos] == None:
                                    # if not added in possible moves
                                    if new_pos not in valid_moves:
                                        valid_moves += [new_pos]
                                else:
                                    break
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
                            if field[new_pos] == None:
                                # if not added in possible moves
                                if new_pos not in valid_moves:
                                    valid_moves += [new_pos]

            attacks = field[pos].get_attack_positions()
            for x, y, endless in attacks:
                if endless:
                    new_x = self.numerical_field_to_alphabetic(lines[pos[0]])
                    new_y = int(pos[1])
                    while True:
                        new_x = self.numerical_field_to_alphabetic(lines[new_x]+x)
                        new_y += y
                        if new_x != None:
                            new_pos = f"{new_x}{new_y}"
                            # position in field
                            if new_pos in positions:
                                # field is enemy
                                if field[new_pos] != None:
                                    if field[new_pos].site != field[pos].site:
                                        # if not added in possible moves
                                        if new_pos not in valid_moves:
                                            valid_moves += [new_pos]
                                            break
                                    else:
                                        break
                                else:
                                    pass
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
                            if field[new_pos] != None and field[new_pos].site != field[pos].site:
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

    def king_pos(self, field, site):
        for pos in positions:
            if field[pos] != None:
                if field[pos].chessman == chessmen.KING and field[pos].site == site:
                    return pos

    def is_check(self, field, site) -> bool:
        """Checks if the givin site is in check"""
        king_pos = self.king_pos(field, site)
        if king_pos != None:
            for pos in positions:
                if field[pos] != None and field[pos].site != site:
                    if king_pos in self.valid_moves(field, pos):
                        return True
            return False
        else:
            pass
            # no king

    # is working? -> or false used
    def is_check_mate(self, field:dict, site) -> bool:
        """Checks if the givin site is in checkmate"""
        # is there no legal move without dangerous the king?
        king_pos = self.king_pos(field, site)
        if king_pos != None:
            # search a turn which endanger the king
            for pos in positions:
                    if field[pos] != None and field[pos].site == site:
                        for to_pos in self.valid_moves(field, pos):
                            copy_field = self.move_without_changes(field, pos, to_pos)
                            if not self.is_check(copy_field, site):
                                return False
            return True
        else:
            pass
            # no king

    def get_opposite_site(self, op_site):
        if op_site == site.WHITE:
            return site.BLACK
        else:
            return site.WHITE
