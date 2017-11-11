import game_logic
import random

"""
Naive algorithm that uses any random direction.
"""

def getNextMove(matrix):
    """Return one of the dir_ constants from game_logic"""

    return random.choice(game_logic.all_directions)
