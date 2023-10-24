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
    CountX = 0
    CountO = 0 
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                CountX += 1
            elif board[i][j] == O:
                CountO +=1

    if CountX == CountO:
        return X
    return O  


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_moves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_moves.add((i,j))
    
    if len(possible_moves) == 0:
        return None
    return possible_moves



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if action not in actions(board):
        raise Exception('Invalid action')
        
    i, j = action
    board_copy = copy.deepcopy(board)
    board_copy[i][j] = player(board)
    return board_copy


def check_row(board, player):
    for i in range(3):
        if board[i][0] == player and board[i][1] == player and board[i][2] == player:
            return True
    return False


def check_column(board, player):
    for i in range(3):
        if board[0][i] == player and board[1][i] == player and board[2][i] == player:
            return True
    return False


def check_diagonal_1(board, player):
    counter = 0
    for i in range(3):
        if board[i][i] == player:
            counter += 1
    if counter == 3:
        return True
    return False


def check_diagonal_2(board, player):
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True
    return False
        

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if check_row(board, X) or check_column(board, X) or check_diagonal_1(board, X) or check_diagonal_2(board, X):
        return X
    elif check_row(board, O) or check_column(board, O) or check_diagonal_1(board, O) or check_diagonal_2(board, O):
        return O
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0
    

def max_value(board):
    v = -math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    v = math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    # Case of player X (max-player)
    elif player(board) == X:
        plays = []
        # Loop over the possible actions
        for action in actions(board):
            # Add in plays list a tuple with the min-value and the action that results to its value
            plays.append([min_value(result(board, action)), action])
        # Reverse sort for the plays list and get the action that should take
        return sorted(plays, key=lambda x:x[0], reverse=True)[0][1]
    
    # Case of player O (min-player)
    elif player(board) == O:
        plays = []
        # Loop over the possible actions
        for action in actions(board):
            plays.append([max_value(result(board, action)), action])
        return sorted(plays, key=lambda x: x[0])[0][1]

    
    
    

