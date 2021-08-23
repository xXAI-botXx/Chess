import abc
from enum import Enum

from Engine.chess_engine import site, chessmen


class Chessman(abc.ABC):
    def __init__(self, site:site, chessman:chessmen):
        self.site = site
        self.chessman = chessman

    @abc.abstractclassmethod
    def get_move_points(self) -> list:
        pass
        # returns the move set from a abstract position
        # [(x-Direction, y-Directon, endless), ...]    -> endless in this direction
        # or
        # [(lines, rows, endless), ...]

    @abc.abstractclassmethod
    def get_attack_points(self) -> list:
        pass


class Pawn(Chessman):
    def __init__(self, site:site, double_move_activated=False, double_jump_possible=True):
        super().__init__(site, chessmen.PAWN)
        self.double_jump_activated = double_move_activated    # by loading you have to check in moves
        self.double_jump_possible = double_jump_possible

    def get_move_points(self) -> list:
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

    def get_attack_points(self) -> list:
        if self.site == site.WHITE:
            return []
        elif self.site == site.BLACK:
            return []


class Rook(Chessman):
    def __init__(self, site:site):
        super().__init__(site, chessmen.PAWN)

    def get_move_points(self) -> list:
        if self.site == site.WHITE:
            return []
        elif self.site == site.BLACK:
            return []

    def get_attack_points(self) -> list:
        if self.site == site.WHITE:
            return []
        elif self.site == site.BLACK:
            return []

    
class Bishop(Chessman):
    def __init__(self, site:site):
        super().__init__(site, chessmen.PAWN)

    def get_move_points(self) -> list:
        if self.site == site.WHITE:
            return []
        elif self.site == site.BLACK:
            return []

    def get_attack_points(self) -> list:
        if self.site == site.WHITE:
            return []
        elif self.site == site.BLACK:
            return []


class Knight(Chessman):
    def __init__(self, site:site):
        super().__init__(site, chessmen.PAWN)

    def get_move_points(self) -> list:
        if self.site == site.WHITE:
            return []
        elif self.site == site.BLACK:
            return []

    def get_attack_points(self) -> list:
        if self.site == site.WHITE:
            return []
        elif self.site == site.BLACK:
            return []

        
class Queen(Chessman):
    def __init__(self, site:site):
        super().__init__(site, chessmen.PAWN)

    def get_move_points(self) -> list:
        if self.site == site.WHITE:
            return []
        elif self.site == site.BLACK:
            return []

    def get_attack_points(self) -> list:
        if self.site == site.WHITE:
            return []
        elif self.site == site.BLACK:
            return []


class King(Chessman):
    def __init__(self, site:site):
        super().__init__(site, chessmen.PAWN)

    def get_move_points(self) -> list:
        if self.site == site.WHITE:
            return []
        elif self.site == site.BLACK:
            return []

    def get_attack_points(self) -> list:
        if self.site == site.WHITE:
            return []
        elif self.site == site.BLACK:
            return []
