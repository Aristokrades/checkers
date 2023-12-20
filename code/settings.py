from math import ceil

FPS = 69

VERTICAL_OFFSET = 0
WIN_WIDTH, WIN_HEIGHT = 750, 750

LIST_SIZE = 8

SQUARE_SIZE = ceil(WIN_WIDTH / LIST_SIZE) if WIN_WIDTH < WIN_HEIGHT else ceil(WIN_HEIGHT / LIST_SIZE) # I know that it can look a little bit weird, but I need to do this in order to eventually run the code on my phone if i'd like to

WHITE_SQUARE_COLOR = '#F5E6BF'
BLACK_SQUARE_COLOR = '#66443A'

BOARD = [
    ['E', 'r', 'E', 'r', 'E', 'r', 'E', 'r',],
    ['r', 'E', 'r', 'E', 'r', 'E', 'E', 'E',],
    ['E', 'r', 'E', 'r', 'E', 'r', 'E', 'r',],
    ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E',],
    ['E', 'r', 'E', 'r', 'E', 'E', 'E', 'E',],
    ['w', 'E', 'w', 'E', 'w', 'E', 'w', 'E',],
    ['E', 'w', 'E', 'r', 'E', 'w', 'E', 'w',],
    ['w', 'E', 'w', 'E', 'E', 'E', 'w', 'E',],
]
