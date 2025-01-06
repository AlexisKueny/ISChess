#
# Example function to be implemented for Single important function is next_best color: a single character str
# indicating the color represented by this bot ('w' for white) board: a 2d matrix containing strings as a descriptors
# of the board '' means empty location "XC" means a piece represented by X of the color C is present there budget:
# time budget allowed for this turn, the function must return a pair (xs,ys) --> (xd,yd) to indicate a piece at xs,
# ys moving to xd, yd
#
from typing import Tuple

from PyQt6 import QtCore

# ----------------
# Setup
# ----------------
from Bots.ADRKChessBotList import register_chess_bot
import Bots.ADRKChessRules
import copy
import random


# ----------------
# Bot functions
# ----------------
def example_chess_bot(player_sequence: str, board, time_budget, **kwargs):
    color = player_sequence[1]
    for x in range(board.shape[0] - 1):
        for y in range(board.shape[1]):
            if board[x, y] != "p" + color:
                continue
            if y > 0 and board[x + 1, y - 1] != '' and board[x + 1, y - 1][-1] != color:
                # Cap piece on right
                return (x, y), (x + 1, y - 1)
            if y < board.shape[1] - 1 and board[x + 1, y + 1] != '' and board[x + 1, y + 1][1] != color:
                # Cap piece on left
                return (x, y), (x + 1, y + 1)
            elif board[x + 1, y] == '':
                # Move chess piece on square forward
                return (x, y), (x + 1, y)

    return (0, 0), (0, 0)


def stupid_bot(player_sequence: str, board, time_budget, **kwargs):
    color = player_sequence[1]
    best_move = (0, 0), (0, 0)
    best_value = -float('inf') if color == 'w' else float('inf')
    reset_val = copy.deepcopy(board)

    for move in findLegalMoves(board, color, player_sequence):
        board = copy.deepcopy(reset_val)
        # Test move
        start_x = move[0][0]
        start_y = move[0][1]
        move_x = move[1][0]
        move_y = move[1][1]
        board[move_x][move_y] = board[start_x][start_y]
        board[start_x][start_y] = ""
        move_eval = evaluate_board(board)

        # Evaluate move
        if color == "w":
            if move_eval > best_value:
                best_value = move_eval
                best_move = (start_x, start_y), (move_x, move_y)
        else:
            if move_eval < best_value:
                best_value = move_eval
                best_move = (start_x, start_y), (move_x, move_y)

    return best_move


def ADRK_random_bot(player_sequence: str, board, time_budget, **kwargs):
    color = player_sequence[1]
    moves = findLegalMoves(board, color, player_sequence)
    i = random.randrange(0, len(moves) - 1)
    return moves[i]


def ADRK_bot(player_sequence: str, board, time_budget, **kwargs):
    """
    Minimax bot that uses the Minimax algorithm to choose the best move.
    :param player_sequence: Sequence string
    :param board: Chess board
    :param time_budget: Time budget allowed for this turn
    :return: The best move
    """
    color = player_sequence[1]
    best_move = None
    best_value = -float('inf') if color == 'w' else float('inf')
    depth = 2  # Set the depth of the Minimax algorithm

    legal_moves = findLegalMoves(board, color, player_sequence)
    print(legal_moves)

    for move in legal_moves:
        board_copy = copy.deepcopy(board)
        make_move(board_copy, move)
        eval = minimax(board_copy, depth - 1, color, player_sequence)

        if color == "w" and eval > best_value:
            best_value = eval
            best_move = move
        elif color == "b" and eval < best_value:
            best_value = eval
            best_move = move

    # Ensure we do not return (0, 0), (0, 0) as a move
    return best_move if best_move else legal_moves[0]


# ----------------
# Helper functions
# ---------------
def findLegalMoves(board, currentPlayer, player_sequence):
    """
    Finds possible legal moves for each piece in the board
    :param board: Chess board
    :param currentPlayer: White/ black player
    :param player_sequence:  seq string
    :return:
    """
    piece_moves = {}

    count = 0
    for y in range(board.shape[0]):
        for x in range(board.shape[1]):
            if currentPlayer in str(board[y][x]):
                piece_moves[str(board[y][x]) + str(count)] = [(y, x)]
                count += 1

    # Matching each piece with possible moves

    for piece in piece_moves:
        for y in range(board.shape[0]):
            for x in range(board.shape[1]):
                start = piece_moves[piece][0]
                end = (y, x)
                move = (start, end)
                try:
                    if Bots.ADRKChessRules.move_is_valid(player_sequence, move, board):
                        piece_moves[piece].append(move[1])
                except IndexError:
                    continue

    moves = []

    for m in piece_moves.values():
        for j in range(1, len(m)):
            moves.append((m[0], m[j]))

    return moves


def evaluate_board(board):
    """
    Function to evaluate score based on all pieces on the board
    """
    global piece
    piece_values = {
        "p": 1,
        "n": 3,
        "b": 3,
        "r": 5,
        "q": 9,
        "k": 10000,
    }

    # Evaluation score
    score = 0

    # Iterate over all the pieces on the board and sum the values
    for x in range(board.shape[0]):
        for y in range(board.shape[1]):
            piece = board[x, y]
            try:
                piece_value = piece_values[piece[0]]
            except IndexError:
                continue
            if piece[1] == 'b':
                score -= piece_value
            else:
                score += piece_value

    return score


def minimax(board, depth, maximizing_player, player_sequence):
    """
    Minimax algorithm to choose the best move.
    :param board: Chess board
    :param depth: Depth of the search tree
    :param maximizing_player: True if the current turn is the maximizing player's turn
    :param player_sequence: Sequence string
    :return: Evaluation score of the board
    """
    if depth == 0 or is_game_over(board):
        return evaluate_board(board)

    legal_moves = findLegalMoves(board, maximizing_player, player_sequence)

    if not legal_moves:
        return evaluate_board(board)

    if maximizing_player == "w":
        max_eval = -float('inf')
        for move in legal_moves:
            board_copy = copy.deepcopy(board)
            make_move(board_copy, move)
            eval = minimax(board_copy, depth - 1, "b", player_sequence)
            max_eval = max(max_eval, eval)
        return max_eval

    elif maximizing_player == 'b':
        min_eval = float('inf')
        for move in legal_moves:
            board_copy = copy.deepcopy(board)
            make_move(board_copy, move)
            eval = minimax(board_copy, depth - 1, "w", player_sequence)
            min_eval = min(min_eval, eval)
        return min_eval


def make_move(board, move):
    """
    Make a move on the board.
    :param board: Chess board
    :param move: A tuple ((start_x, start_y), (end_x, end_y))
    """
    start_x, start_y = move[0]
    end_x, end_y = move[1]
    board[end_x][end_y] = board[start_x][start_y]
    board[start_x][start_y] = ""


def is_game_over(board):
    """
    Checks if the game is over by looking for checkmate, stalemate, or other conditions.
    :param board: Chess board
    :return: True if the game is over, False otherwise
    """
    # Checkmate, stalemate, or other conditions can be implemented based on your specific game rules
    # For simplicity, let's assume the game is over if a king is missing
    kings = {'w': False, 'b': False}
    for x in range(board.shape[0]):
        for y in range(board.shape[1]):
            if board[x, y] == 'kw':
                kings['w'] = True
            elif board[x, y] == 'kb':
                kings['b'] = True

    # If either king is missing, the game is over
    return not kings['w'] or not kings['b']


# -------------------
# Bot registration
# -------------------

register_chess_bot("ADRK", ADRK_bot)
register_chess_bot("ADRK_Random", ADRK_random_bot)
