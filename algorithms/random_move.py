from game_logic import all_directions
import random

"""
Naive algorithm that uses any random direction.
"""


def get_next_move(matrix):
    """Return one of the dir_ constants from game_logic"""

    return random.choice(all_directions)
