import copy


PLAYER_X = "X"
PLAYER_O = "O"


def is_free_to_mark(board, movement):
    x, y = movement
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
    x=0
    for row in board:
        y=0
        for column in row:
            if column is None:
                rest+=[(x,y)]
            y+=1 
        x+=1
    return rest

"""
Returns the state after taking action a in state s
"""
def result(board, action):
    x,y = action
    dibujo = players(board)
    if is_free_to_mark(board, action):
        new_board = copy.deepcopy(board)
        new_board[y][x] = dibujo
        return new_board
    
    return board

    
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
            return board[x][0]
        if board[0][x] is not None and board[0][x] == board[1][x] == board[2][x]:
            return board[0][x]
        
    if board[0][0] is not None and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] is not None and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]
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

    if w == PLAYER_X:
        return 1
    elif w == PLAYER_O:
        return -1
    else:
        return 0  