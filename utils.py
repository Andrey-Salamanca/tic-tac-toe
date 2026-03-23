import copy


PLAYER_X = "X"
PLAYER_O = "O"


def is_free_to_mark(board, movement):
    y, x = movement
    return board[x][y] is None

"""
Returns the player who must move in state s
"""
def players(board):
    cont =0
    for row in board:
        for cell in row:
            if cell is not None:
                cont += 1
    
    if cont % 2 == 0:
        return PLAYER_X
    else:
        return PLAYER_O

"""
Returns the legal moves in state s
"""
def actions(board):
    rest=[]
    for x in range(3):
        for y in range(3):
            if board[x][y] is None:
                rest+=[(y,x)]
    return rest

"""
Returns the state after taking action a in state s
"""
def result(board, action):
    y,x = action
    
    new_board = copy.deepcopy(board)
    new_board[x][y] = players(board)
    return new_board


    
"""
Checks whether state s is a terminal state
gana en linea horizontal, vertical o diagonal
"""
def draw(board):
    for row in board:
        for cell in row:
            if cell is None:
                return False
    return True

def winner (board):
    for x in range(3):
        if board[x][0] is not None and board[x][0] == board[x][1] == board[x][2]:
            return [(x,0),(x,1),(x,2)]
        if board[0][x] is not None and board[0][x] == board[1][x] == board[2][x]:
            return [(0,x),(1,x),(2,x)]
        
    if board[0][0] is not None and board[0][0] == board[1][1] == board[2][2]:
        return [(0,0),(1,1),(2,2)]
    if board[0][2] is not None and board[0][2] == board[1][1] == board[2][0]:
        return [(0,2),(1,1),(2,0)]
    return None

def terminal(board):
    if winner(board) is not None:
        return True

    return draw(board)

"""
Final numeric value for terminal state s
"""

def utility(board):
    w = winner(board)
    if w is None:     
        return 0 
    row, col = w[0]         
    if board[row][col] == PLAYER_X:
        return 1
    if board[row][col] == PLAYER_O:
        return -1
