import numpy as np
import pygame
import sys
import math
import random
from threading import Timer
from functions import Board as brd

#################################
# GLOBAL CONSTANTS             
#################################

ROWS = 6
COLS = 7

# Constants for easy coloring of elements
# RGB color codes
BROWN = (199, 138, 58)
BLACK = (0, 0, 0)
RED = (199, 58, 58)
BLUE = (58, 62, 199)

BRIGHT_RED = (255, 168, 190)
BRIGHT_BLUE = (168, 229, 255)


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

# Initializing the board
board = brd.gen_board(ROWS, COLS)

# Variable for looping through the game loop until someone wins
game_over = False

# Variable flag for the game loop used for the pygame GUI
not_over = True

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

# initialy it is player 1's turn
turn = random.randint(0, 1)

pygame.init()
pygame.display.set_caption("Player vs Player - ZANTE")
SQUARESIZE = 75

width = COLS * SQUARESIZE
height = (ROWS + 1) * SQUARESIZE
circle_radius = int(SQUARESIZE/2 - 5)

size = (width, height)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

default_font = pygame.font.SysFont("consolas", 30)



# game loop
# -------------------------------

# loop that runs while the game_over variable is false,
# ie someone hasn't placed 4 in a row yet
while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION and not_over:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            xpos = pygame.mouse.get_pos()[0]

            if turn == 0:
                pygame.draw.circle(screen, RED, (xpos, int(SQUARESIZE/2)), circle_radius )
            else: 
                pygame.draw.circle(screen, BLUE, (xpos, int(SQUARESIZE/2)), circle_radius )

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN and not_over:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            # ask for player 1 inupt
            if turn == 0:
                # we assume players will use correct input
                xpos = event.pos[0] 
                col = int(math.floor(xpos/SQUARESIZE)) #int(input("Player 1 make your selection by typing (0-6):"))

                if brd.col_still_has_space(board, col).any():
                    row = brd.get_next_open_space(board, col, ROWS)
                    brd.place_piece(board, row, col, 1)

                    if brd.is_winning_move(board, 1, ROWS, COLS):
                        brd.highlight_winning_move(board, 1, ROWS, COLS)
                        end_game("PLAYER 1 WINS!", RED)
                else:
                    end_game("DRAW", BROWN)

            # ask for player 2 input
            else:
                xpos = event.pos[0] 
                col = int(math.floor(xpos/SQUARESIZE)) #int(input("Player 2 make your selection by typing (0-6):"))

                if brd.col_still_has_space(board, col).any():
                    row = brd.get_next_open_space(board, col, ROWS)
                    brd.place_piece(board, row, col, 2)

                    if brd.is_winning_move(board, 2, ROWS, COLS):
                        brd.highlight_winning_move(board, 2, ROWS, COLS)
                        end_game("PLAYER 2 WINS!", BLUE)
                else:
                    end_game("DRAW", BROWN)

            draw_board(board)

            # increment turn by 1
            turn += 1
            # this will alternate between 0 and 1 withe very turn
            turn = turn % 2
