from enum import Enum

import chess_men as chess
from chess_engine import positions, site, modes

class Field(object):
    def __init__(self, field=dict(), moves=[], new_game=True, mode=modes.CLASSIC):
        self.field = field
        self.moves = moves
        self.mode = mode

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

    def move(self):
        pass
