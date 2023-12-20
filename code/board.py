from settings import *
from square import Square
from piece import Piece

class Board:
    'Board class which has to draw the actuall board and all the pieces'
    def __init__(self, display_surface):
        self.display_surface = display_surface

    def clear_marked(self, piece_map):
         for row in range(LIST_SIZE):
            for col in range(LIST_SIZE):
                if piece_map[row][col] == 'm': piece_map[row][col] = 'E'

    def display_board(self):
        for row in range(LIST_SIZE):
            for col in range(LIST_SIZE):
                if row % 2 == 1 and col % 2 == 1 or row % 2 == 0 and col % 2 == 0:
                    x = col * SQUARE_SIZE
                    y = row * SQUARE_SIZE       
                    square = Square(x, y, WHITE_SQUARE_COLOR)
                    self.display_surface.blit(square.image, square.rect)

    def display_pieces(self, piece_map):
        for row in range(LIST_SIZE):
            for col in range(LIST_SIZE):
                x = col * SQUARE_SIZE
                y = row * SQUARE_SIZE
                type = piece_map[row][col]
                if type != "E": 
                    piece = Piece(x, y, type)
                    self.display_surface.blit(piece.image, piece.rect)

    def display(self, map):
        self.display_board()
        self.display_pieces(map)