from game_logic import merge, all_directions, score

"""
This algorithm tests which direction results in the highest score and chooses greedily.
"""

def get_next_move(matrix):
    """Return one of the dir_ constants from game_logic"""

    def get_value(mat):
        # Tuple ordering prefers earlier values.
        # Here we prefer new matricies, then higher-score matricies.
        return (mat != matrix, score(mat))

    best_value, best_direction = max(
        (get_value(merge(matrix, direction)), direction)
        for direction in all_directions
    )

    return best_direction
