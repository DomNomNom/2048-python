from game_logic import dir_up, dir_down, dir_left, dir_right, merge, all_directions, score, find_empty_positions,set_value, reverse_each_row, transpose

import math

import random
random.seed(4)

"""
Tries to avoid paths that lead to constricting options.
"""

# dir_tiebreaker = {
#     dir_right: 4,
#     dir_down: 3,
#     dir_left: 2,
#     dir_up: 1,
# }

samples_remaining = None  # initialized in get_next_move

# def even_distribute(num_balls, num_boxes):
#     base_amount, uneven_amount = divmod(num_balls, num_boxes)
#     boxes = [
#         base_amount+1 if i<uneven_amount else base_amount
#         for i in range(num_boxes)
#     ]
#     random.shuffle(boxes)
#     assert sum(boxes) == num_balls
#     return boxes

# Puts balls into buckets such that the distribution looks like
# the distribution of the weights
def distribute(num_balls, weights):
    distributed_amounts = []
    total_weights = sum(weights)
    for weight in weights:
        weight = float(weight)
        p = weight / total_weights
        distributed_amount = round(p * num_balls)
        distributed_amounts.append(distributed_amount)
        total_weights -= weight
        num_balls -= distributed_amount
    return distributed_amounts


def my_score(matrix):
    return len(find_empty_positions(matrix))*10000 + score(matrix)

def fills_and_num_samples(mat, max_samples):
    '''
    >>> list(fills_and_num_samples( ((0,4,4,4),(4,4,4,4),(4,4,4,4),(4,4,4,4)), 100))
    [(((0, 0), 4), 10), (((0, 0), 2), 90)]
    >>> list(fills_and_num_samples( ((0,4,4,4),(4,4,0,4),(4,4,4,4),(4,4,4,4)), 200))
    [(((1, 2), 4), 10), (((1, 2), 2), 90), (((0, 0), 2), 90), (((0, 0), 4), 10)]
    '''
    empty_positions = find_empty_positions(mat)
    fills_and_weights = (
        [((pos, 2), 9) for pos in empty_positions] +
        [((pos, 4), 1) for pos in empty_positions]
    )
    random.shuffle(fills_and_weights)
    fills   = [f_w[0] for f_w in fills_and_weights]
    weights = [f_w[1] for f_w in  fills_and_weights]
    num_samples = distribute(max_samples, weights)

    return zip(fills, num_samples)

dirs_and_weights = [
    (dir_down, 1),
    (dir_right, 1),
    (dir_left, 1),
    (dir_up, 1),
]
def directions_and_samples(matrix, max_samples):
    # random.shuffle(dirs_and_weights)
    dirs    = [f_w[0] for f_w in dirs_and_weights]
    weights = [f_w[1] for f_w in  dirs_and_weights]
    num_samples = distribute(max_samples, weights)
    return zip(dirs, num_samples)

def combine_dir_scores(scores):
    return max(scores)
def combine_fill_scores(scores):
    average = sum(scores) / float(len(scores))
    return min(scores) * 0.99 + average * 0.01


def get_value_of_move(matrix, direction, max_samples=200):

    mat = merge(matrix, direction)
    if mat == matrix:
        return 0

    if max_samples <= 1:
        return my_score(matrix)
    del matrix  # avoid mistakes

    fill_scores = []
    sample_count = 0
    for fill, fill_samples in fills_and_num_samples(mat, max_samples):
        if not fill_samples:
            continue
        # do fill, recurse on filled matrix.
        filled_mat = set_value(mat, fill[0], fill[1])
        dir_scores = []
        for new_dir, dir_samples in directions_and_samples(filled_mat, fill_samples):
            new_value = get_value_of_move(filled_mat, new_dir, dir_samples)
            dir_scores.append(new_value)
            sample_count += dir_samples
        fill_scores.append(combine_dir_scores(dir_scores))
    assert sample_count == max_samples
    return combine_fill_scores(fill_scores)
    # return my_score(mat)


def get_next_move(starting_matrix):
    """Return one of the dir_ constants from game_logic"""

    best_value, best_direction = max(
        (get_value_of_move(starting_matrix, direction), direction)
        for direction in all_directions
    )


    return best_direction
