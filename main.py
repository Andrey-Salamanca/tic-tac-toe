# import math
from minimax import ai_play,max_value
from utils import result


board = [
    ["X", "X", None],
    ["O", "O", None],
    ["X", "X", None],
]


def play():
    board = [
        ["X", "X", None],
        ["O", None, None],
        [None, None, None],
    ]
    result = max_value(board)
    print(result)

play()
