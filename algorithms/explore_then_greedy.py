from game_logic import dir_up, dir_down, dir_left, dir_right, merge, all_directions, score, find_empty_positions,set_value, reverse_each_row, transpose

import math

import random
random.seed(4)

"""
minimax by distributing samples of where to explore.
"""

samples_remaining = None  # initialized in get_next_move

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

def get_fills_and_num_samples(mat, max_samples):
    '''
    >>> list(get_fills_and_num_samples( ((0,4,4,4),(4,4,4,4),(4,4,4,4),(4,4,4,4)), 100))
    [(((0, 0), 4), 10), (((0, 0), 2), 90)]
    >>> list(get_fills_and_num_samples( ((0,4,4,4),(4,4,0,4),(4,4,4,4),(4,4,4,4)), 200))
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

def combine_fill_scores(scores):
    average = sum(scores) / float(len(scores))
    return min(scores) * 0.99 + average * 0.01


def get_value_of_post_move(mat, max_samples):
    if max_samples <= 1:
        return my_score(mat)

    fills_and_num_samples = get_fills_and_num_samples(mat, max_samples)
    if not fills_and_num_samples:
        # return 0
        return my_score(mat)

    fill_scores = []
    sample_count = 0
    for fill, fill_samples in fills_and_num_samples:
        if not fill_samples:
            continue
        # do fill, recurse on filled matrix.
        filled_mat = set_value(mat, fill[0], fill[1])
        fill_scores.append(get_value_and_move(filled_mat, fill_samples)[0])
        sample_count += fill_samples
    assert sample_count == max_samples

    return combine_fill_scores(fill_scores)
    # return my_score(mat)

def get_explore_weights(merged_matrices):
    return [1] * len(merged_matrices)


def get_value_and_move(starting_matrix, max_samples=1000):

    if max_samples <= 1:
        return (my_score(starting_matrix), dir_down)


    merged_states = [ (merge(starting_matrix, direction), direction) for direction in all_directions ]
    valid_states = [ (mat, direction) for (mat, direction) in merged_states if mat != starting_matrix]
    weights = get_explore_weights([ mat for mat,direction in valid_states ])
    num_samples_per_state = distribute(max_samples, weights)

    if not valid_states:
        # return 0
        return (my_score(starting_matrix), dir_down)

    dir_scores = []
    sample_count = 0
    for (mat, direction), num_samples in zip(valid_states, num_samples_per_state):
        if not num_samples:
            continue
        new_value = get_value_of_post_move(mat, num_samples)
        dir_scores.append(new_value)
        sample_count += num_samples
    rankables = [ (score, direction) for score, (mat, direction) in zip(dir_scores, valid_states) ]
    return max(rankables)

def get_next_move(starting_matrix):
    """Return one of the dir_ constants from game_logic"""

    best_value, best_direction = get_value_and_move(starting_matrix)

    return best_direction
