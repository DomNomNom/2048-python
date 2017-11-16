from game_logic import merge, dir_up, dir_down, dir_left, dir_right

"""
Simple example algorithm, that tries to gather cells in bottom right corner.
"""
prioritized_directions = [dir_down, dir_right, dir_left, dir_up]

def get_next_move(matrix):
    """Return one of the dir_ constants from game_logic"""

    for direction in prioritized_directions:
        if merge(matrix, direction) != matrix:
            return direction

    return dir_down  # no good options
