#
# Example function to be implemented for Single important function is next_best color: a single character str
# indicating the color represented by this bot ('w' for white) board: a 2d matrix containing strings as a descriptors
# of the board '' means empty location "XC" means a piece represented by X of the color C is present there budget:
# time budget allowed for this turn, the function must return a pair (xs,ys) --> (xd,yd) to indicate a piece at xs,
# ys moving to xd, yd
#

from PyQt6 import QtCore

#   Be careful with modules to import from the root (don't forget the Bots.)
from Bots.ChessBotList import register_chess_bot
import ChessRules
import shutil


#   Simply move the pawns forward and tries to capture as soon as possible
def example_chess_bot(player_sequence: str, board, time_budget, **kwargs):
    color = player_sequence[1]
    print(findLegalMoves(board, color, player_sequence))
    print(evaluate_board(board))
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


def greedy_bot(player_sequence: str, board, time_budget, **kwargs):
    print("Greedy bot says hello")
    color = player_sequence[1]
    best_move = (0, 0), (0, 0)
    best_value = -float('inf') if color == 'w' else float('inf')

    for move in findLegalMoves(board, color, player_sequence):
        print("Scanning moves")
        # Test move
        start_x = move[0][0]
        start_y = move[0][1]
        move_x = move[1][0]
        move_y = move[1][1]
        print(f"Trying move from ({start_x},{start_y}) to ({move_x},{move_y})")

        board[move_x][move_y] = board[start_x][start_y]
        board[start_x][start_y] = "--"
        print("Evaluating move")
        move_eval = evaluate_board(board)
        print("Eval completed")

        # Evaluate move
        if color == "w":
            if move_eval > best_value:
                print("Better move for white found")
                best_value = move_eval
                best_move = (start_x,start_y),(move_x, move_y)
                print(best_move)
        else:
            if move_eval < best_value:
                print("Better move for black found")
                best_value = move_eval
                best_move = (start_x,start_y),(move_x,move_y)

    return best_move


def findLegalMoves(board, currentPlayer, player_sequence):
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
                    if ChessRules.move_is_valid(player_sequence, move, board):
                        piece_moves[piece].append(move[1])
                except IndexError:
                    continue

    moves = []

    for m in piece_moves.values():
        for j in range(1, len(m)):
            moves.append((m[0], m[j]))

    print("Hello from findLegalMoves")
    print(moves)

    return moves


def evaluate_board(board):
    """ Function to evaluate score based on all pieces on the board
    """
    global piece
    piece_values = {
        "p": 1,
        "n": 3,
        "b": 3,
        "r": 5,
        "q": 9,
        "k": 1000,
        "-": 0
    }

    # Evaluation score
    score = 0

    # Iterate over all the pieces on the board and sum the values
    for x in range(board.shape[0]):
        for y in range(board.shape[1]):
            piece = board[x, y]
            try:
                piece_value = piece_values[piece[0]]
                print(piece_value)
            except IndexError:
                continue
            if piece[1] == 'b':
                score -= piece_value
            else:
                score += piece_value

    return score


#  Example how to register the function
register_chess_bot("Greedy", greedy_bot)
