import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count == o_count else O


def actions(board):
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions


def result(board, action):
    i, j = action
    if board[i][j] != EMPTY:
        raise Exception("Invalid action")
    new_board = copy.deepcopy(board)
    new_board[i][j] = player(board)
    return new_board


def winner(board):

    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not None:
            return row[0]

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            return board[0][col]

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    return None


def terminal(board):
    if winner(board) is not None:
        return True
    for row in board:
        if EMPTY in row:
            return False
    return True


def utility(board):
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0

def minimax(board):
    if terminal(board):
        return None

    current_player = player(board)

    if current_player == X:
        value, move = max_value(board)
    else:
        value, move = min_value(board)
    return move

def max_value(board):
    if terminal(board):
        return utility(board), None

    v = -math.inf
    best_move = None
    for action in actions(board):
        new_value, _ = min_value(result(board, action))
        if new_value > v:
            v = new_value
            best_move = action
            if v == 1:
                break
    return v, best_move

def min_value(board):
    if terminal(board):
        return utility(board), None

    v = math.inf
    best_move = None
    for action in actions(board):
        new_value, _ = max_value(result(board, action))
        if new_value < v:
            v = new_value
            best_move = action
            if v == -1:
                break
    return v, best_move

