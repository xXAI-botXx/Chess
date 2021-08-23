import abc
from enum import Enum

from Engine.chess_engine import site, chessmen


class Chessman(abc.ABC):
    def __init__(self, site:site, chessman:chessmen, name:str, kills=[]):
        self.site = site
        self.chessman = chessman
        self.name = name
        self.kills = kills

    @abc.abstractclassmethod
    def get_move_positions(self) -> list:
        pass
        # returns the move set from a abstract position
        # [(x-Direction, y-Directon, endless), ...]    -> endless in this direction
        # or
        # [(lines, rows, endless), ...]

    @abc.abstractclassmethod
    def get_attack_positions(self) -> list:
        pass

    def get_name(self) -> str:
        return self.name.title()

    def get_kills(self) -> int:
        return len(self.kills)

    def add_kill(self, enemie:str) -> str:
        self.kills += [enemie]


class Pawn(Chessman):
    def __init__(self, site:site, double_move_activated=False, double_jump_possible=True, kills=[]):
        super().__init__(site, chessmen.PAWN, "pawn", kills)
        self.double_jump_activated = double_move_activated    # by loading you have to check in moves
        self.double_jump_possible = double_jump_possible

    def get_move_positions(self) -> list:
        if self.site == site.WHITE:
            if self.double_jump_possible and not self.double_jump_activated:
                return [(0, 1, False), (0, 2, False)]
            else:
                return [(0, 1, False)]
        elif self.site == site.BLACK:
            if self.double_jump_possible and not self.double_jump_activated:
                return [(0, -1, False), (0, -2, False)]
            else:
                return [(0, -1, False)]

    def get_attack_positions(self) -> list:
        if self.site == site.WHITE:
            return [(1, 1, False), (-1, 1, False)]
        elif self.site == site.BLACK:
            return [(1, -1, False), (-1, -1, False)]


class Rook(Chessman):
    def __init__(self, site:site, kills=[]):
        super().__init__(site, chessmen.ROOK, "rook", kills)

    def get_move_positions(self) -> list:
        return [(0, 1, True), (1, 0, True), (0, -1, True), (-1, 0, True)]

    def get_attack_positions(self) -> list:
        return [(0, 1, True), (1, 0, True), (0, -1, True), (-1, 0, True)]

    
class Bishop(Chessman):
    def __init__(self, site:site, kills=[]):
        super().__init__(site, chessmen.BISHOP, "bishop", kills)

    def get_move_positions(self) -> list:
        return [(1, 1, True), (-1, 1, True), (1, -1, True), (-1, -1, True)]

    def get_attack_positions(self) -> list:
        return [(1, 1, True), (-1, 1, True), (1, -1, True), (-1, -1, True)]


class Knight(Chessman):
    def __init__(self, site:site, kills=[]):
        super().__init__(site, chessmen.KNIGHT, "knight", kills)

    def get_move_positions(self) -> list:
        return [(1, 2, False), (-1, 2, False), (1, -2, False), (-1, -2, False)]

    def get_attack_positions(self) -> list:
        return [(1, 2, False), (-1, 2, False), (1, -2, False), (-1, -2, False)]

        
class Queen(Chessman):
    def __init__(self, site:site, kills=[]):
        super().__init__(site, chessmen.QUEEN, "queen", kills)

    def get_move_positions(self) -> list:
        return [(1, 1, True), (-1, 1, True), (1, -1, True), (-1, -1, True), (0, 1, True), (1, 0, True), (0, -1, True), (-1, 0, True)]

    def get_attack_positions(self) -> list:
        return [(1, 1, True), (-1, 1, True), (1, -1, True), (-1, -1, True), (0, 1, True), (1, 0, True), (0, -1, True), (-1, 0, True)]


class King(Chessman):
    def __init__(self, site:site, kills=[]):
        super().__init__(site, chessmen.KING, "king", kills)

    def get_move_positions(self) -> list:
        return [(0, 1, False), (0, -1, False), (1, 0, False), (-1, 0, False)]

    def get_attack_positions(self) -> list:
        return [(0, 1, False), (0, -1, False), (1, 0, False), (-1, 0, False)]

