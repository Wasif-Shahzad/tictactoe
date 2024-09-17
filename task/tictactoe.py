"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if terminal(board):
        return 'S'
    cnt = 0
    for row in board:
        for piece in row:
            if piece != EMPTY:
                cnt += 1
    if cnt % 2 == 0:
        return 'X'
    else:
        return 'O'


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    set_of_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                set_of_actions.add((i, j))
    return set_of_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    x, y = action
    if x >= 3 or y >= 3 or x < 0 or y < 0 or board[x][y] != EMPTY:
        raise Exception("Invalid actions")
    new_board = copy.deepcopy(board)
    move = player(board)
    new_board[x][y] = move
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    for i in range(3):
        for j in range(3):
            if board[i][j] != EMPTY:
                for dx, dy in directions:
                    consecutive = [(i, j)]
                    for k in range(1, 3):
                        ni, nj = i + k * dx, j + k * dy
                        if 0 <= ni < 3 and 0 <= nj < 3 and board[ni][nj] == board[i][j]:
                            consecutive.append((ni, nj))
                        else:
                            break
                    if len(consecutive) == 3:
                        return board[i][j]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    cnt = 0
    for row in board:
        for piece in row:
            if piece != EMPTY:
                cnt += 1
    if cnt == 9:
        return True
    return winner(board) is not None


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == 'X':
        return 1
    elif win == 'O':
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    player_to_move = player(board)
    if player_to_move == 'X':
        best = -2
        optimal_moves = None
        for move in actions(board):
            # print(move)
            new_state = result(board, move)
            value = minimax_value(new_state)
            if value > best:
                best = value
                optimal_moves = move
        return optimal_moves
    else:
        best = 2
        optimal_moves = None
        for move in actions(board):
            new_state = result(board, move)
            value = minimax_value(new_state)
            if value < best:
                best = value
                optimal_moves = move
        return optimal_moves


def minimax_value(board):
    if terminal(board):
        return utility(board)
    player_to_move = player(board)
    if player_to_move == 'X':
        best = -2
        for move in actions(board):
            new_board = result(board, move)
            best = max(best, minimax_value(new_board))
            if best == 1:
                break
        return best
    else:
        best = 2
        for move in actions(board):
            new_board = result(board, move)
            best = min(best, minimax_value(new_board))
            if best == -1:
                break
        return best
