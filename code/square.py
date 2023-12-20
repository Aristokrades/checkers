from pygame import Surface

from settings import SQUARE_SIZE

class Square:
    'Class for every square on the board (for now only black)'
    def __init__(self, x, y, color):
        self.image = Surface((SQUARE_SIZE, SQUARE_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = (x, y))
