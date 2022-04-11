import numpy as np
import pygame
import sys
import math
from threading import Timer
import random

#################################
# GLOBAL VARIABLES              
#################################

# Board's size (X and Y)
ROWS = 6
COLS = 7

# Constants to determine who's turn it is
PLAYER_TURN = 0
AI_TURN = 1

# Constant to represent the player's pieces
# Player's piece 1 == color RED
# AI's piece 2 == color BLUE
# These are 1 and 2 since 0 would represent an empty space
PLAYER_PIECE = 1
AI_PIECE = 2

# Constants for easy coloring of elements
# RGB color codes
BROWN = (199, 138, 58)
BLACK = (0, 0, 0)
RED = (199, 58, 58)
BLUE = (58, 62, 199)

#################################
# FUNCTIONS             
#################################

# Function to create a board based on the ROWS and COLS constants
def gen_board():
    board = np.zeros((ROWS, COLS))
    return board


# Function to place a player's piece on the passed location
def place_piece(board, row, col, piece):
    board[row][col] = piece


# Function to check if the columns first/top row is empty
def col_still_has_space(board, col):
    return board[0][col] == 0


# Function to get the next empty/open space in a column
def get_next_open_space(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == 0:
            return r


# calculating if the current state of the board for player or AI is a win
def is_winning_move(board, piece):
    # checking horizontal 'windows' of 4 for win
    for c in range(COLS-3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # checking vertical 'windows' of 4 for win
    for c in range(COLS):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # checking positively sloped diagonals for win
    for c in range(COLS-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

    # checking negatively sloped diagonals for win
    for c in range(3,COLS):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c-1] == piece and board[r-2][c-2] == piece and board[r-3][c-3] == piece:
                return True


# Function to highlight the 4 connected pieces for the winning player
def highlight_winning_move(board, piece):
    if piece == 1:
        winning_piece = 3
    else:
        winning_piece = 4
    # checking horizontal 'windows' of 4 for win
    for c in range(COLS-3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                board[r][c] = winning_piece
                board[r][c+1] = winning_piece
                board[r][c+2] = winning_piece
                board[r][c+3] = winning_piece

    # checking vertical 'windows' of 4 for win
    for c in range(COLS):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                board[r][c] = winning_piece
                board[r+1][c] = winning_piece
                board[r+2][c] = winning_piece
                board[r+3][c] = winning_piece

    # checking positively sloped diagonals for win
    for c in range(COLS-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                board[r][c] = winning_piece
                board[r-1][c+1] = winning_piece
                board[r-2][c+2] = winning_piece
                board[r-3][c+3] = winning_piece

    # checking negatively sloped diagonals for win
    for c in range(3,COLS):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c-1] == piece and board[r-2][c-2] == piece and board[r-3][c-3] == piece:
                board[r][c] = winning_piece
                board[r-1][c-1] = winning_piece
                board[r-2][c-2] = winning_piece
                board[r-3][c-3] = winning_piece


# visually representing the board using pygame
# for each position in the matrix the board is either filled with an empty black circle, or a palyer/AI red/yellow circle
def draw_board(board):
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BROWN, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE ))
            if board[r][c] == 0:
                pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE/2), int(r* SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)
            elif board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE/2), int(r* SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)
            elif board[r][c] == 2 :
                pygame.draw.circle(screen, BLUE, (int(c * SQUARESIZE + SQUARESIZE/2), int(r* SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)
    pygame.display.update()


# evaluate a 'window' of 4 locations in a row based on what pieces it contains
# the values used can be experimented with
def evaluate_window(window, piece):
    # by default the oponent is the player
    opponent_piece = PLAYER_PIECE

    # if we are checking from the player's perspective, then the oponent is AI
    if piece == PLAYER_PIECE:
        opponent_piece = AI_PIECE

    # initial score of a window is 0
    score = 0

    # based on how many friendly pieces there are in the window, we increase the score
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    # or decrese it if the oponent has 3 in a row
    if window.count(opponent_piece) == 3 and window.count(0) == 1:
        score -= 4 

    return score    


# scoring the overall attractiveness of a board after a piece has been droppped
def score_position(board, piece):

    score = 0

    # score center column --> we are prioritizing the central column because it provides more potential winning windows
    center_array = [int(i) for i in list(board[:,COLS//2])]
    center_count = center_array.count(piece)
    score += center_count * 6

    # below we go over every single window in different directions and adding up their values to the score
    # score horizontal
    for r in range(ROWS):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLS - 3):
            window = row_array[c:c + 4]
            score += evaluate_window(window, piece)

    # score vertical
    for c in range(COLS):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROWS-3):
            window = col_array[r:r+4]
            score += evaluate_window(window, piece)

    # score positively sloped diagonals
    for r in range(3,ROWS):
        for c in range(COLS - 3):
            window = [board[r-i][c+i] for i in range(4)]
            score += evaluate_window(window, piece)

    # score negatively sloped diagonals
    for r in range(3,ROWS):
        for c in range(3,COLS):
            window = [board[r-i][c-i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score

# checking if the given turn or in other words node in the minimax tree is terminal
# a terminal node is player winning, AI winning or board being filled up
def is_terminal_node(board):
    return is_winning_move(board, PLAYER_PIECE) or is_winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0


# The algorithm calculating the best move to make given a depth of the search tree.
# Depth is how many layers algorithm scores boards. Complexity grows exponentially.
# Alpha and beta are best scores a side can achieve assuming the opponent makes the best play.
# More on alpha-beta pruning here: https://www.youtube.com/watch?v=l-hh51ncgDI.
# maximizing_palyer is a boolean value that tells whether we are maximizing or minimizing
# in this implementation, AI is maximizing.
def minimax(board, depth, alpha, beta, maximizing_player):

    # all valid locations on the board
    valid_locations = get_valid_locations(board)

    # boolean that tells if the current board is terminal
    is_terminal = is_terminal_node(board)

    # if the board is terminal or depth == 0
    # we score the win very high and a draw as 0
    if depth == 0 or is_terminal:
        if is_terminal: # winning move 
            if is_winning_move(board, AI_PIECE):
                return (None, 10000000)
            elif is_winning_move(board, PLAYER_PIECE):
                return (None, -10000000)
            else:
                return (None, 0)
            #Singit ng pang change ng color ng mga winnig pieces
            

        # if depth is zero, we simply score the current board
        else: # depth is zero
            return (None, score_position(board, AI_PIECE))

    # if the current board is not rerminal and we are maximizing
    if maximizing_player:

        # initial value is what we do not want - negative infinity
        value = -math.inf

        # this will be the optimal column. Initially it is random
        column = random.choice(valid_locations)

        # for every valid column, we simulate dropping a piece with the help of a board copy
        # and run the minimax on it with decresed depth and switched player
        for col in valid_locations:
            row = get_next_open_space(board, col)
            b_copy = board.copy()
            place_piece(b_copy, row, col, AI_PIECE)
            # recursive call
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            # if the score for this column is better than what we already have
            if new_score > value:
                value = new_score
                column = col
            # alpha is the best option we have overall
            alpha = max(value, alpha) 
            # if alpha (our current move) is greater (better) than beta (opponent's best move), then 
            # the oponent will never take it and we can prune this branch
            if alpha >= beta:
                break

        return column, value
    
    # same as above, but for the minimizing player
    else: # for thte minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_space(board, col)
            b_copy = board.copy()
            place_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(value, beta) 
            if alpha >= beta:
                break
        return column, value


# get all columns where a piece can be
def get_valid_locations(board):
    valid_locations = []
    
    for column in range(COLS):
        if col_still_has_space(board, column):
            valid_locations.append(column)

    return valid_locations


# end the game which will close the window eventually
def end_game():
    global game_over
    game_over = True
    print(game_over)


# various state tracker variables taht use the above fucntions
# -------------------------------

# initializing the board
board = gen_board()

# initially nobody has won yet
game_over = False

# initially the game is not over - this is used for GUI quirks
not_over = True

# initial turn is random
turn = random.randint(PLAYER_TURN, AI_TURN)

# initializing pygame
pygame.init()

# size of one game location
SQUARESIZE = 75

# dimensions for pygame GUI
width = COLS * SQUARESIZE
height = (ROWS + 1) * SQUARESIZE
circle_radius = int(SQUARESIZE/2 - 5)
size = (width, height)
screen = pygame.display.set_mode(size)

# font for win message
my_font = pygame.font.SysFont("consolas", 30)

# draw GUI
draw_board(board)
pygame.display.update()


# game loop
# -------------------------------

# loop that runs while the game_over variable is false,
# i.e., someone hasn't placed 4 in a row yet
while not game_over:

    if turn == PLAYER_TURN and not game_over and not_over:

        # the column to drop in is found using minimax
        col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

        if col_still_has_space(board, col):
            pygame.time.wait(500)
            row = get_next_open_space(board, col)
            place_piece(board, row, col, PLAYER_PIECE)
            if is_winning_move(board, PLAYER_PIECE):
                print("GIT GUD HUMAN! AI WINS!")
                label = my_font.render("GIT GUD HUMAN! AI WINS!", 1, RED)
                screen.blit(label, (40, 10))
                not_over = False
                t = Timer(3.0, end_game)
                t.start()
        else:
            print("DRAW! NICE!")
            label = my_font.render("DRAW! NICE!", 1, BROWN)
            screen.blit(label, (40, 10))
            not_over = False
            t = Timer(3.0, end_game)
            t.start()
        draw_board(board)    

        # increment turn by 1
        turn += 1
        # this will alternate between 0 and 1 withe very turn
        turn = turn % 2
                     
    # if its the AI's turn
    if turn == AI_TURN and not game_over and not_over:

        # the column to drop in is found using minimax
        col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

        if col_still_has_space(board, col).any():
            pygame.time.wait(500)
            row = get_next_open_space(board, col)
            place_piece(board, row, col, AI_PIECE)
            if is_winning_move(board, AI_PIECE):
                print("GIT GUD HUMAN! AI WINS!")
                label = my_font.render("GIT GUD HUMAN! AI WINS!", 1, BLUE)
                screen.blit(label, (40, 10))
                not_over = False
                t = Timer(3.0, end_game)
                t.start()
        else:
            print("DRAW! NICE!")
            label = my_font.render("DRAW! NICE!", 1, BROWN)
            screen.blit(label, (40, 10))
            not_over = False
            t = Timer(3.0, end_game)
            t.start()
        draw_board(board)    

        # increment turn by 1
        turn += 1
        # this will alternate between 0 and 1 withe very turn
        turn = turn % 2
