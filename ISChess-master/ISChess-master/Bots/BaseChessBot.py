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


#   Simply move the pawns forward and tries to capture as soon as possible
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


def pawn_mover_bot(player_sequence: str, board, time_budget, **kwargs):
    color = player_sequence[1]
    print("color", color)
    piece_moves = {}
    print("board dimensions", board.shape)
    print(board)

    # Populating dictionary with pieces
    count = 0
    for y in range(board.shape[0]):
        for x in range(board.shape[1]):
            print(str(board[y][x]))
            if color in str(board[y][x]):
                piece_moves[str(board[y][x])+str(count)] = [(y, x)]
                count += 1
    print(piece_moves)

    # Matching each piece with possible moves

    for piece in piece_moves:
        for y in range(board.shape[0] - 1):
            for x in range(board.shape[1]):
                start = piece_moves[piece][0]
                end = (y, x)
                move = (start, end)
                print(move)
                try:
                    if ChessRules.move_is_valid(player_sequence, move, board):
                        piece_moves[piece].append(move[1])
                except IndexError:
                    continue

    print(piece_moves)

    #find possible moves for each piece
    return (0, 0), (0, 0)


#   Example how to register the function
register_chess_bot("PawnMover", pawn_mover_bot)
