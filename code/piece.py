from pygame import image, transform

from settings import SQUARE_SIZE

class Piece:
    def __init__(self, x, y, type):
        piece_types = {
            "w": "white_pawn",
            "r": "red_pawn",
            "W": "white_queen",
            "R": "red_queen",
            "m": "circle"
        }
        path = "../graphics/"
        base = piece_types[type]
        ext = ".png"        

        self.image = image.load(path + base + ext).convert_alpha()
        self.image = transform.scale(self.image, (SQUARE_SIZE, SQUARE_SIZE))
        
        self.rect = self.image.get_rect(topleft=(x, y))