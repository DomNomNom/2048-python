import game_logic

"""
Simple example algorithm, that tries to gather cells in bottom right corner.
"""

def getNextMove(matrix):
    """Return one of the dir_ constants from game_logic"""

    #  if possible move to right bottom corner
    mat, changed = game_logic.right(matrix)
    if changed: return game_logic.dir_right
    mat, changed = game_logic.down(matrix)
    if changed: return game_logic.dir_down

    #  otherwise try to any other move
    mat, changed = game_logic.left(matrix)
    if changed: return game_logic.dir_left
    return game_logic.dir_up
