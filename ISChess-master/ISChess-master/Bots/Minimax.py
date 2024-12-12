import ChessRules


class Tree:
    def __init__(self):
        self.left = None
        self.right = None
        self.data = None


def findPossibleMoves(board, currentPlayer, player_sequence):
    piece_moves = {}

    count = 0
    for y in range(board.shape[0]):
        for x in range(board.shape[1]):
            print(str(board[y][x]))
            if currentPlayer in str(board[y][x]):
                piece_moves[str(board[y][x]) + str(count)] = [(y, x)]
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
    return piece_moves
