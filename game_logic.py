from math import log
import itertools

dir_up = '^'
dir_down = 'v'
dir_left = '<'
dir_right = '>'
all_directions = [dir_up, dir_down, dir_left, dir_right]


def merge(matrix, direction):
    if direction == dir_up:    return merge_up(matrix)
    if direction == dir_down:  return merge_down(matrix)
    if direction == dir_left:  return merge_left(matrix)
    if direction == dir_right: return merge_right(matrix)
    assert direction in all_directions

def merge_up(matrix):
    return transpose(merge_left(transpose(matrix)))

def merge_down(matrix):
    return merge_up(matrix[::-1])[::-1]  # [::-1] means flip vertically

def merge_left(matrix):
    return tuple(row_merge_left(row) for row in matrix)

def merge_right(matrix):
    return reverse_each_row(merge_left(reverse_each_row(matrix)))

def new_matrix(n=4):
    '''
    >>> new_matrix()
    ((0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0))
    >>> new_matrix(2)
    ((0, 0), (0, 0))
    '''
    return tuple( tuple( 0 for i in range(n) ) for j in range(n) )

def get_value(matrix, position):
    return matrix[position[0]][position[1]]

def set_value(matrix, position, value):
    '''
    Returns a new state matrix with the value being set at the position
    >>> set_value(new_matrix(), (2,3), 4)
    ((0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 4), (0, 0, 0, 0))
    '''
    row_index, col_index = position
    assert 0 <= row_index < len(matrix)
    assert 0 <= col_index < len(matrix)
    return tuple(
        row if i != row_index else tuple(
            existingValue if j != col_index else value
            for j, existingValue in enumerate(row)
        )
        for i, row in enumerate(matrix)
    )

def find_empty_positions(matrix):
    '''
    >>> find_empty_positions( ((0,2,4,4),
    ...                        (8,2,0,4),
    ...                        (4,2,2,4),
    ...                        (8,2,2,4),) )
    [(0, 0), (1, 2)]
    '''
    return [
        (row_index, col_index)
        for row_index, col_index in itertools.product(
            range(len(matrix)),
            range(len(matrix))
        )
        if not matrix[row_index][col_index]
    ]

def score(matrix):
    """ calculated the score
    Adds scores if each cell, where each cell has a score according to:
    2 -> 3
    4 -> 9
    8 -> 27
    ...
    This prioritizes combining.
    """
    total_score = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] > 0:
                total_score += 3 ** log(matrix[i][j], 2)
    return int(total_score)




def row_merge_left(row):
    '''
    >>> row_merge_left((2,2,2,2))
    (4, 4, 0, 0)
    >>> row_merge_left((4,4,8,16))
    (8, 8, 16, 0)
    >>> row_merge_left((2,0,2,2))
    (4, 2, 0, 0)
    >>> row_merge_left((8,4,0,4))
    (8, 8, 0, 0)
    '''
    merged = [ value for value in row if value ]

    # remove any same value that's adjacent
    # but don't process an index twice
    i = 0
    while i < len(merged)-1:
        if merged[i] == merged[i+1]:
            merged[i] *= 2
            del merged[i+1]
        i += 1

    # Pad the end with zeros and convert back to a tuple
    return tuple(merged) + (0,) * (len(row) - len(merged))

def reverse_each_row(mat):
    return tuple(row[::-1] for row in mat)

def transpose(mat):
    return tuple(zip(*mat))



assert len(all_directions) == len(set(all_directions))
if __name__ == '__main__':
    import puzzle
    puzzle.GameGrid()
