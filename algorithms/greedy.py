import game_logic
import random

"""
This algorithm tests which direction results in the highest score and chooses greedily.
If multiple directions have same score, they are ordered by priority.
"""

def getNextMove(matrix):
    """Return one of the dir_ constants from game_logic"""

    max_score = game_logic.score(matrix)
    same_score = []
    for i in ["right","down","left","up"]:
        temp, changed = game_logic.direction(matrix, i)
        if not changed: continue
        this_score = game_logic.score(temp)
        if this_score > max_score:
            max_score = this_score
            same_score = []
        if this_score == max_score:
            same_score.append(i)

    # pick one of possible directions with highest scored according to priorities
    return same_score[0]
