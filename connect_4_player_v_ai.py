# import numpy as np
import pygame
import sys
import math
from threading import Timer
import random
from functions import Board as brd, MiniMax as mm


#################################
# GLOBAL VARIABLES              
#################################

# Board's size (X and Y)
ROWS = 6
COLS = 7

DIFFICULTY = 7

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

BRIGHT_RED = (255, 168, 190)
BRIGHT_BLUE = (168, 229, 255)

#################################
# FUNCTIONS             
#################################


# Function to handle updating the game visuals
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
            elif board[r][c] == 3:
                pygame.draw.circle(screen, BRIGHT_RED, (int(c * SQUARESIZE + SQUARESIZE/2), int(r* SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)
            elif board[r][c] == 4 :
                pygame.draw.circle(screen, BRIGHT_BLUE, (int(c * SQUARESIZE + SQUARESIZE/2), int(r* SQUARESIZE + SQUARESIZE + SQUARESIZE/2)), circle_radius)
    pygame.display.update()


# Function to end the game loop
def end_game(massage, text_color):
    global not_over

    print(massage)
    label = default_font.render(massage, 1, text_color)
    screen.blit(label, (40, 10))
    not_over = False
    t = Timer(5.0, close_window)
    t.start()
    

def close_window():
    global game_over
    game_over = True
    print(game_over)


#################################
# VARIABLES FOR THE GAME LOOP  
#################################

# initializing the board
board = brd.gen_board(ROWS, COLS)

# Variable for looping through the game loop until someone wins
game_over = False

# Variable flag for the game loop used for the pygame GUI
not_over = True

# Variable to select 1 random player to move first
turn = random.randint(PLAYER_TURN, AI_TURN)

# Initialize the pygame
pygame.init()
pygame.display.set_caption("PLAYER vs AI - ZANTE")

# size of one game location
SQUARESIZE = 75

# Variables to determine the size of the game window and other elements
width = COLS * SQUARESIZE
height = (ROWS + 1) * SQUARESIZE
circle_radius = int(SQUARESIZE/2 - 5)
size = (width, height)
screen = pygame.display.set_mode(size)

# Variable to determine the default_font
default_font = pygame.font.SysFont("consolas", 30)

# Update/draw the initial pygame board
draw_board(board)
pygame.display.update()


#################################
# MAIN GAME LOOP
#################################

while not game_over:

    # Checks for player/human input
    for event in pygame.event.get():

        # Check if the game is closed
        if event.type == pygame.QUIT:
            sys.exit()

        # Draw a correspoding colored circle following the player's mouse
        if event.type == pygame.MOUSEMOTION and not_over:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            xpos = pygame.mouse.get_pos()[0]
            if turn == PLAYER_TURN:
                pygame.draw.circle(screen, RED, (xpos, int(SQUARESIZE/2)), circle_radius )

        # Listening for the player click.
        # Places the correspoding colored cicle if true
        if event.type == pygame.MOUSEBUTTONDOWN and not_over:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))

            if turn == PLAYER_TURN:

                # we assume players will use correct input
                xpos = event.pos[0] 
                col = int(math.floor(xpos/SQUARESIZE)) 

                if brd.col_still_has_space(board, col).any():
                    row = brd.get_next_open_space(board, col, ROWS)
                    brd.place_piece(board, row, col, PLAYER_PIECE)
                    if brd.is_winning_move(board, PLAYER_PIECE, ROWS, COLS):
                        brd.highlight_winning_move(board, PLAYER_PIECE, ROWS, COLS)
                        end_game("THERE IS HOPE FOR HUMANITY", RED)
                else:
                    end_game("WOW A DRAW VS AN AI!", BROWN)
                draw_board(board) 

                turn += 1
                # Alternate between 0 and 1
                # value of 0 == PLAYER1 while value of 1 == PLAYER2
                turn = turn % 2 

        pygame.display.update()

                     
    # AI move
    if turn == AI_TURN and not game_over and not_over:

        # the column to drop in is found using minimax
        # minimax_score catches the value of the move.
        col, minimax_score = mm.minimax(board, DIFFICULTY, -math.inf, math.inf, True, ROWS, COLS, PLAYER_PIECE, AI_PIECE)
        
        if brd.col_still_has_space(board, col).any():
            pygame.time.wait(500)
            row = brd.get_next_open_space(board, col, ROWS)
            brd.place_piece(board, row, col, AI_PIECE)
            if brd.is_winning_move(board, AI_PIECE, ROWS, COLS):
                brd.highlight_winning_move(board, AI_PIECE, ROWS, COLS)
                end_game("GIT GUD HUMAN! AI WINS!", BLUE)
        else:
            end_game("GOOD GAME - DRAW", BROWN)
        draw_board(board)

        turn += 1
        # Alternate between 0 and 1
        # value of 0 == PLAYER1 while value of 1 == PLAYER2
        turn = turn % 2
