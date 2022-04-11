import numpy as np
import math
import random


class Board:
    # Function to create a board based on the rows and cols constants
    def gen_board(rows, cols):
        board = np.zeros((rows, cols))
        return board


    # Function to place a player's piece on the passed location
    def place_piece(board, row, col, piece):
        board[row][col] = piece

    
    # Function to check if the columns first/top row is empty
    def col_still_has_space(board, col):
        return board[0][col] == 0


    # Function to get the next empty/open space in a column
    def get_next_open_space(board, col, rows):
        for r in range(rows-1, -1, -1):
            if board[r][col] == 0:
                return r
    

    # calculating if the current state of the board for player or AI is a win
    def is_winning_move(board, piece, rows, cols):
        # checking horizontal 'windows' of 4 for win
        for c in range(cols-3):
            for r in range(rows):
                if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                    return True

        # checking vertical 'windows' of 4 for win
        for c in range(cols):
            for r in range(rows-3):
                if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                    return True

        # checking positively sloped diagonals for win
        for c in range(cols-3):
            for r in range(3, rows):
                if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                    return True

        # checking negatively sloped diagonals for win
        for c in range(3,cols):
            for r in range(3, rows):
                if board[r][c] == piece and board[r-1][c-1] == piece and board[r-2][c-2] == piece and board[r-3][c-3] == piece:
                    return True


    # Function to highlight the 4 connected pieces for the winning player
    def highlight_winning_move(board, piece, rows, cols):
        if piece == 1:
            winning_piece = 3
        else:
            winning_piece = 4

        # checking horizontal 'windows' of 4 for win
        for c in range(cols-3):
            for r in range(rows):
                if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                    board[r][c] = winning_piece
                    board[r][c+1] = winning_piece
                    board[r][c+2] = winning_piece
                    board[r][c+3] = winning_piece

            # checking vertical 'windows' of 4 for win
            for c in range(cols):
                for r in range(rows-3):
                    if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                        board[r][c] = winning_piece
                        board[r+1][c] = winning_piece
                        board[r+2][c] = winning_piece
                        board[r+3][c] = winning_piece

            # checking positively sloped diagonals for win
            for c in range(cols-3):
                for r in range(3, rows):
                    if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                        board[r][c] = winning_piece
                        board[r-1][c+1] = winning_piece
                        board[r-2][c+2] = winning_piece
                        board[r-3][c+3] = winning_piece
            
            # checking negatively sloped diagonals for win
            for c in range(3,cols):
                for r in range(3, rows):
                    if board[r][c] == piece and board[r-1][c-1] == piece and board[r-2][c-2] == piece and board[r-3][c-3] == piece:
                        board[r][c] = winning_piece
                        board[r-1][c-1] = winning_piece
                        board[r-2][c-2] = winning_piece
                        board[r-3][c-3] = winning_piece
    

    # scoring the overall attractiveness of a board after a piece has been droppped
    def score_position(board, piece, rows, cols, player_piece, ai_piece):

        score = 0

        # score center column --> we are prioritizing the central column because it provides more potential winning windows
        center_array = [int(i) for i in list(board[:,cols//2])]
        center_count = center_array.count(piece)
        score += center_count * 6

        # below we go over every single window in different directions and adding up their values to the score
        # score horizontal
        for r in range(rows):
            row_array = [int(i) for i in list(board[r,:])]
            for c in range(cols - 3):
                window = row_array[c:c + 4]
                score += Window.evaluate_window(window, piece, player_piece, ai_piece)

        # score vertical
        for c in range(cols):
            col_array = [int(i) for i in list(board[:,c])]
            for r in range(rows-3):
                window = col_array[r:r+4]
                score += Window.evaluate_window(window, piece, player_piece, ai_piece)

        # score positively sloped diagonals
        for r in range(3,rows):
            for c in range(cols - 3):
                window = [board[r-i][c+i] for i in range(4)]
                score += Window.evaluate_window(window, piece, player_piece, ai_piece)

        # score negatively sloped diagonals
        for r in range(3,rows):
            for c in range(3,cols):
                window = [board[r-i][c-i] for i in range(4)]
                score += Window.evaluate_window(window, piece, player_piece, ai_piece)

        return score
    
    # checking if the given turn or in other words node in the minimax tree is terminal
    # a terminal node is player winning, AI winning or board being filled up
    def is_terminal_node(board, rows, cols, player_piece, ai_piece):
        return Board.is_winning_move(board, player_piece, rows, cols) or Board.is_winning_move(board, ai_piece, rows, cols) or len(Board.get_valid_locations(board, cols)) == 0


    # get all columns where a piece can be
    def get_valid_locations(board, cols):
        valid_locations = []
        
        for column in range(cols):
            if Board.col_still_has_space(board, column):
                valid_locations.append(column)

        return valid_locations


class Window:
    # evaluate a 'window' of 4 locations in a row based on what pieces it contains
    # the values used can be experimented with
    def evaluate_window(window, piece, player_piece, ai_piece):
        # by default the oponent is the player
        opponent_piece = player_piece

        # if we are checking from the player's perspective, then the oponent is AI
        if piece == player_piece:
            opponent_piece = ai_piece

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


class MiniMax:
    # is_maxing_player == to check if we are maximizing the player or minimizing
    def minimax(board, depth, alpha, beta, is_maxing_player, rows, cols, player_piece, ai_piece):

        # all valid locations on the board
        valid_locations = Board.get_valid_locations(board, cols)

        # boolean that tells if the current board is terminal
        is_terminal = Board.is_terminal_node(board, rows, cols, player_piece, ai_piece)

        # if the board is terminal or depth == 0
        # we score the win very high and a draw as 0
        if depth == 0 or is_terminal:
            if is_terminal: # winning move 
                if Board.is_winning_move(board, ai_piece, rows, cols):
                    return (None, 10000000)
                elif Board.is_winning_move(board, player_piece, rows, cols):
                    return (None, -10000000)
                else:
                    return (None, 0)
                #Singit ng pang change ng color ng mga winnig pieces
                

            # if depth is zero, we simply score the current board
            else: # depth is zero
                return (None, Board.score_position(board, ai_piece, rows, cols, player_piece, ai_piece))

        # if the current board is not rerminal and we are maximizing
        if is_maxing_player:

            # initial value is what we do not want - negative infinity
            value = -math.inf

            # this will be the optimal column. Initially it is random
            column = random.choice(valid_locations)

            # for every valid column, we simulate dropping a piece with the help of a board copy
            # and run the minimax on it with decresed depth and switched player
            for col in valid_locations:
                row = Board.get_next_open_space(board, col, rows)
                b_copy = board.copy()
                Board.place_piece(b_copy, row, col, ai_piece)
                # recursive call
                new_score = MiniMax.minimax(b_copy, depth-1, alpha, beta, False, rows, cols, player_piece, ai_piece)[1]
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
                row = Board.get_next_open_space(board, col, rows)
                b_copy = board.copy()
                Board.place_piece(b_copy, row, col, player_piece)
                new_score = MiniMax.minimax(b_copy, depth-1, alpha, beta, True, rows, cols, player_piece, ai_piece)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(value, beta) 
                if alpha >= beta:
                    break
            return column, value