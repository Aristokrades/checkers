import pygame
from sys import exit
from copy import deepcopy

from settings import *
from board import Board

class Game:
    'The game mechanic'
    def __init__(self):

        pygame.init()
        self.clock = pygame.time.Clock()

        self.display_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("checkers")

        self.board = Board(self.display_surface)
        self.piece_map = deepcopy(BOARD)
        self.analizing_board = deepcopy(BOARD)
        self.display_surface.fill(BLACK_SQUARE_COLOR)
        
        # Key boolean values
        self.is_multi_capturing = False
        self.white_on_turn = True
        self.has_to_take = None

        self.i = 0
        self.logs = [[(0, 0), 'E']]
        self.clicks_on_same = 0

    def can_pawn_in_given_direction(self, type_of_piece: str, row: int, col: int, direction: str):
        counter = 0
        current_row = row
        current_col = col
        attack_cords = ()
        if type_of_piece == 'w': enemy_pieces = ['r', 'R']
        elif type_of_piece == 'r': enemy_pieces = ['w', 'W']
        if type_of_piece == 'w' and self.white_on_turn or type_of_piece == 'r' and not self.white_on_turn: # so we are talking about a pawn
            match direction:
                case "topleft":
                    if current_row >= 2 and current_col >= 2 and self.analizing_board[current_row-1][current_col-1] in enemy_pieces and self.analizing_board[current_row-2][current_col-2] == 'E': 
                        self.analizing_board[current_row-1][current_col-1] = 'E'
                        current_row = current_row-2
                        current_col = current_col-2
                        counter+=1
                case "topright":
                    if current_row >= 2 and current_col < LIST_SIZE-2 and self.analizing_board[current_row-1][current_col+1] in enemy_pieces and self.analizing_board[current_row-2][current_col+2] == 'E': 
                        self.analizing_board[current_row-1][current_col+1] = 'E'
                        current_row = current_row-2
                        current_col = current_col+2             
                        counter+=1
                case "botleft":
                    if current_row < LIST_SIZE-2 and current_col >= 2 and self.analizing_board[current_row+1][current_col-1] in enemy_pieces and self.analizing_board[current_row+2][current_col-2] == 'E': 
                        self.analizing_board[current_row+1][current_col-1] = 'E'
                        current_row = current_row+2
                        current_col = current_col-2               
                        counter += 1
                case "botright":
                    if current_row < LIST_SIZE-2 and current_col < LIST_SIZE-2 and self.analizing_board[current_row+1][current_col+1] in enemy_pieces and self.analizing_board[current_row+2][current_col+2] == 'E': 
                        self.analizing_board[current_row+1][current_col+1] = 'E'
                        current_row = current_row+2
                        current_col = current_col+2
                        counter += 1
        if counter !=0: counter += self.check_if_pawn_can_capture(type_of_piece, current_row, current_col)[0]
        return [counter, (current_row, current_col)]

    def check_if_pawn_can_capture(self, type_of_piece: str, row: int, col: int):
        options = ["topleft", "topright", "botleft", "botright"]
        counter = 0
        output_cords = []
        for option in options:
            temporary_counter, temporary_cords = self.can_pawn_in_given_direction(type_of_piece, row, col, option)
            if temporary_counter == counter and counter !=0:
                output_cords.append(temporary_cords)
            if temporary_counter > counter: 
                counter = temporary_counter
                output_cords.clear()
                output_cords.append(temporary_cords)

        return [counter, output_cords]

    def check_if_queen_can_capture(self, type_of_piece, row, col):
        pass

    def who_must_capture(self):
        output_cords = []
        attack_squares = []
        maximum = 0
        for row in range(LIST_SIZE):
            for col in range(LIST_SIZE): 
                type_of_piece = self.piece_map[row][col]
                self.analizing_board = deepcopy(self.piece_map)
                if type_of_piece in ['w', 'r']: # so if we are talking about pawn
                    attacks, attack_square = self.check_if_pawn_can_capture(type_of_piece, row, col)
                    # *
                    # - Printing for fun
                    # *
                    player = "białego" if self.white_on_turn else "czerwonego"
                    if attacks != 0: print(f"Zawodnik grający bierkami koloru {player} może użyć bierki o położeniu ({row},{col}), aby zdobyć następującą ilość bierek przeciwnika: {attacks}")
                    # *
                    # - The end of print, I will delete it later on
                    # *
                    if attacks == maximum and attacks != 0: 
                        output_cords.append((row, col)) 
                        attack_squares.append(attack_square)
                    elif attacks > maximum: 
                        maximum = attacks
                        output_cords.clear()
                        attack_squares.clear()
                        output_cords.append((row, col))
                        attack_squares.append(attack_square)
                elif type_of_piece in ['W', 'R']: # so we are talking about a queen
                    # attacks, attack_square = self.check_if_queen_can_capture(type_of_piece, row, col)
                    pass
        
        return [output_cords, attack_squares]

    def draw_moving_possibilities_for_pawn(self, row, col):
        if col-1 >= 0 and self.piece_map[row][col-1] == 'E':  self.piece_map[row][col-1] = 'm' # im checking here if col-1 in order to prevent piece from row 0 from teleporting lol
        if col+1 < LIST_SIZE and self.piece_map[row][col+1] == 'E': self.piece_map[row][col+1] = 'm'

    def draw_moving_possibilities_for_queen(self, row, col):

        def draw_moving_possibilities_for_queen_in_given_direction(start_row, end_row, start_col, end_col, step_row, step_col):
            current_col = start_col
            for current_row in range(start_row, end_row, step_row):
                print("row ", current_row, "col ", current_col, "piece_type ", self.piece_map[6][1] if current_col < LIST_SIZE else "")

                if current_col < LIST_SIZE and self.piece_map[current_row][current_col] == 'E': self.piece_map[current_row][current_col] = 'm' # and col >= 0 and row >= 0
                # elif self.piece_map[current_row][current_col] in ['w', 'W', 'r', 'R']: return
                else: 
                    print("-------", "")
                    return
                    
                current_col += step_col

        
        # bottom right direction
        if (row < LIST_SIZE-1 and col < LIST_SIZE-1): draw_moving_possibilities_for_queen_in_given_direction(row+1, LIST_SIZE-row, col+1, LIST_SIZE-col, 1, 1)
        
        # bottom left direction
        if (row < LIST_SIZE-1 and col > 0): draw_moving_possibilities_for_queen_in_given_direction(row+1, LIST_SIZE-row, col-1, 0, 1, -1)
        
        # top right direction        
        if (row > 0 and col < LIST_SIZE-1): draw_moving_possibilities_for_queen_in_given_direction(row-1, 0, col+1, LIST_SIZE-1, -1, 1)
        
        # top left direction
        if (row > 0 and col > 0): draw_moving_possibilities_for_queen_in_given_direction(row-1, 0, col-1, 0, -1, -1)
    
    def draw_attacking_possibilities_for_pawn(self, row: int, col: int, able_to_attack: list, enemy_pieces: list):
        if row >= 2 and col >= 2 and self.piece_map[row-1][col-1] in enemy_pieces and self.piece_map[row-2][col-2] == 'E' and [(row-2, col-2)] in able_to_attack[1]: self.piece_map[row-2][col-2] = 'm'
        if row >= 2 and col < LIST_SIZE-2 and self.piece_map[row-1][col+1] in enemy_pieces and self.piece_map[row-2][col+2] == 'E' and [(row-2, col+2)] in able_to_attack[1]: self.piece_map[row-2][col+2] = 'm'
        if row < LIST_SIZE-2 and col >= 2 and self.piece_map[row+1][col-1] in enemy_pieces and self.piece_map[row+2][col-2] == 'E' and [(row+2, col-2)] in able_to_attack[1]: self.piece_map[row+2][col-2] = 'm'
        if row < LIST_SIZE-2 and col < LIST_SIZE-2 and self.piece_map[row+1][col+1] in enemy_pieces and self.piece_map[row+2][col+2] == 'E' and [(row+2, col+2)] in able_to_attack[1]: self.piece_map[row+2][col+2] = 'm'

    def move_pawn(self, row: int, picked_row: int, col: int, picked_col: int, player_pawn: str, player_queen: str, queen_row: int):
        # pawns movement (if is after moving)
        self.piece_map[row][col] = player_pawn if row != queen_row else player_queen # promote to queen if at last rank
        self.piece_map[picked_row][picked_col] = 'E'
        self.swap_players()

    def promote(self, row: int, col: int, queen_row: int, before_queen_row: int, take_before_queen_row: int, player_queen: str, player_pawn: str, enemy_pieces: list):
        # if is after taking opponent piece and is at last rank and cannot take another piece then promote; else just be a pawn
        if row == queen_row and not ((col > 2 and self.piece_map[before_queen_row][col-1] in enemy_pieces and self.piece_map[take_before_queen_row][col-2] == 'E') or (
            col < LIST_SIZE-2 and self.piece_map[before_queen_row][col+1] in enemy_pieces and self.piece_map[take_before_queen_row][col+2] == 'E')): 
                self.piece_map[row][col] = player_queen
        else: 
            self.piece_map[row][col] = player_pawn

    def check_multi_capture(self, row, col, player_pawn):
        self.analizing_board[row][col] = player_pawn
        if ((row, col)) not in self.who_must_capture()[0]: 
            self.swap_players()
            self.is_multi_capturing = False
            self.has_to_take = None
        else: 
            self.is_multi_capturing = True
            self.has_to_take = (row, col)

    def clear_enemy_pawn_after_taking(self, row: int, picked_row: int, col: int, picked_col: int, player_pawn: str):
        if picked_row >= 2 and picked_col >= 2 and picked_row-2 == row and picked_col-2 == col: 
            self.piece_map[picked_row-1][picked_col-1] = 'E'
            self.check_multi_capture(row, col, player_pawn)
        elif picked_row >= 2 and picked_col < LIST_SIZE-2 and picked_row-2 == row and picked_col+2 == col: 
            self.piece_map[picked_row-1][picked_col+1] = 'E'
            self.check_multi_capture(row, col, player_pawn)
        elif picked_row < LIST_SIZE-2 and picked_col >= 2 and picked_row+2 == row and picked_col-2 == col:
            self.piece_map[picked_row+1][picked_col-1] = 'E'
            self.check_multi_capture(row, col, player_pawn)
        elif picked_row < LIST_SIZE-2 and picked_col < LIST_SIZE-2 and picked_row+2 == row and picked_col+2 == col:
            self.piece_map[picked_row+1][picked_col+1] = 'E'
            self.check_multi_capture(row, col, player_pawn)

    def react_to_player_input(self, row: int, col: int, type_of_piece: str, picked: list):
        # unpacking the "picked" variable, which contains valuable information about our picked piece; that is its position on the board and its type
        picked_row = picked[0][0]
        picked_col = picked[0][1]
        picked_type = picked[1]

        # here I make some variables to use them in moving logic below
        if self.white_on_turn:
            player_pawn = 'w'
            player_queen = 'W'
            enemy_pawn = 'r'
            enemy_queen = 'R'
            actuall_row = picked_row - 1
            queen_row = 0
            before_queen_row = queen_row + 1
            take_before_queen_row = queen_row + 2
        else: 
            player_pawn = 'r'
            player_queen = 'R'
            enemy_pawn = 'w'
            enemy_queen = 'W'
            actuall_row = picked_row + 1
            queen_row = 7
            before_queen_row = queen_row-1
            take_before_queen_row = queen_row-2
        enemy_pieces = [enemy_pawn, enemy_queen]

        # getting from what position can player attack (returns empty list if can't)
        able_to_attack = self.who_must_capture()
        print(able_to_attack)
        print(able_to_attack[0])
        print(able_to_attack[1])
        print(self.has_to_take)

        # the whole logic:
        if type_of_piece == player_pawn: # so we are selecting the pawn
            if able_to_attack == [[], []]: self.draw_moving_possibilities_for_pawn(actuall_row, col) # if nothing can attack, then just move
            elif ((row, col)) in able_to_attack[0] and (self.has_to_take == None or self.has_to_take == (row, col)): self.draw_attacking_possibilities_for_pawn(row, col, able_to_attack, enemy_pieces) # if can attack
        
        elif type_of_piece == player_queen: # so we are selecting queen
            if able_to_attack == [[], []]:  self.draw_moving_possibilities_for_queen(row, col)

        elif type_of_piece == 'm': # if we are changing location of selected piece
            if picked_type == player_pawn: # so well, if we are doing something with a pawn to get to one of possible squares
                if actuall_row == row and (picked_col-1 == col or picked_col+1 == col): self.move_pawn(row, picked_row, col, picked_col, player_pawn, player_queen, queen_row) # mving the pawn if cannot attack
                # pawns capturing (if is not after moving = is after taking)
                else: self.promote(row, col, queen_row, before_queen_row, take_before_queen_row, player_queen, player_pawn, enemy_pieces)
                
                # capturing
                self.piece_map[picked_row][picked_col] = 'E' # cleaning the square, where attacking piece is
                self.clear_enemy_pawn_after_taking(row, picked_row, col, picked_col, player_pawn)

        # if you click on the same piece twice, the marked points should disappear
        if picked == self.logs[-1]: self.clicks_on_same += 1
        else: self.clicks_on_same = 0

        if self.clicks_on_same % 2 == 1: self.board.clear_marked(self.piece_map)

        self.logs.append([(row, col), type_of_piece])

    def swap_players(self): self.white_on_turn = False if self.white_on_turn else True

    def game_loop(self):
        picked = [(0, 2), 'E'] # just to fix tis error that sayin' "picked is not assigned" (or sth like that) when trynna pick nothing at move first
        self.board.display(self.piece_map)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # cleaning board
                    self.display_surface.fill(BLACK_SQUARE_COLOR)

                    # getting list of posisiton and type of clicked piece (or mark) from mouse input
                    click_x = event.pos[0]
                    click_y = event.pos[1]
                    row = click_y // SQUARE_SIZE
                    col = click_x // SQUARE_SIZE
                    type_of_piece = self.piece_map[row][col]

                    # clear all the purple dots
                    self.board.clear_marked(self.piece_map)

                    # getting what piece has been choosen
                    if self.white_on_turn and type_of_piece in ['w', 'W'] or not self.white_on_turn and type_of_piece in ['r', 'R']: 
                        picked = [(row, col), type_of_piece] 

                    

                    # and well, reacting to click
                    self.react_to_player_input(row, col, type_of_piece, picked)

                    # drawing all pieces and the board
                    self.board.display(self.piece_map)

            pygame.display.update()
            self.clock.tick(FPS)