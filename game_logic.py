from math import log

dir_up = 0
dir_down = 1
dir_left = 2
dir_right = 3
all_directions = [dir_up, dir_down, dir_left, dir_right]
for direction in all_directions:
    assert 0 <= direction < 4  # We depend on this in add_to_random_state()
assert len(all_directions) == len(set(all_directions))


#
# There should be at least 16 seed actions.
class GameModel(object):

    # public

    def __init__(self, seedDirections):
        self.mat = new_matrix()

        self.random_state = 1
        for seed in seedDirections:
            self.add_to_random_state(seed)

        self.add_tile()
        self.add_tile()


    def do_swipe(self, direction):
        assert direction in all_directions
        self.mat,changed = swipe(self.mat, direction)
        if not changed:
            return self.mat,changed
        self.add_to_random_state(direction)
        self.add_tile()
        return self.mat,changed

    # private

    def add_tile(self):
        # pick an empty tile and put a 2 (sometimes 4) there.
        empties = []
        for row in range(len(self.mat)):
            for col in range(len(self.mat)):
                if self.mat[row][col] == 0:
                    empties.append((row, col))
        row,col = empties[self.rand_mod(len(empties))]
        new_value = 2 if self.rand_mod(10)>0 else 4
        self.mat[row][col] = new_value
        return self.mat

    random_state_bitwidth = 32  # simulate random_state being kept in a uint32
    random_state_bitmask = 2**random_state_bitwidth - 1
    def add_to_random_state(self, direction):
        assert direction in all_directions
        self.random_state = ((self.random_state << 2) | direction) & self.random_state_bitmask

    def rand_mod(self, mod):
        self.prng_step()
        return self.random_state % mod

    # takes a step in the pseudo random number generator
    def prng_step(self):
        # Does steps of of a fibonacci LFSR
        # https://en.wikipedia.org/wiki/Linear-feedback_shift_register#Fibonacci_LFSRs
        # This PRNG method was chosen due to it being simple to implement and not terrible.
        lfsr = self.random_state
        for i in range(self.random_state_bitwidth):
            bit = 1 & ((lfsr >> 0) ^ (lfsr >> 2) ^ (lfsr >> 3) ^ (lfsr >> 5) )
            lfsr =  (lfsr >> 1) | (bit << (self.random_state_bitwidth - 1))
        assert lfsr == lfsr & self.random_state_bitmask
        self.random_state = lfsr


# A new sqare matrix with the given sidelength
def new_matrix(n=4):
    return [ [ 0 for i in range(n) ] for j in range(n) ]



def swipe(mat, direction):
    if direction == dir_up:    return up(mat)
    if direction == dir_down:  return down(mat)
    if direction == dir_left:  return left(mat)
    if direction == dir_right: return right(mat)

def up(mat):
    mat = transpose(mat)
    mat,changed = left(mat)
    mat = transpose(mat)
    return (mat,changed)

def down(mat):
    mat = reverse(transpose(mat))
    mat,changed = left(mat)
    mat = transpose(reverse(mat))
    return (mat,changed)

def left(mat):
    mat,changed_fall1 = fall_to_left(mat)
    mat,changed_merge = merge_horizontal_adjacent_same(mat)
    mat,changed_fall2 = fall_to_left(mat)
    return (mat, changed_fall1 or changed_merge or changed_fall2)

def right(mat):
    mat = reverse(mat)
    mat,changed = left(mat)
    mat = reverse(mat)
    return (mat,changed)




def fall_to_left(mat):
    new = new_matrix(len(mat))
    changed = False
    for row in range(len(mat)):
        fall_to_col = 0  # where the next non-zero value will be placed
        for col in range(len(mat)):
            if mat[row][col] == 0:
                continue
            new[row][fall_to_col] = mat[row][col]
            if col != fall_to_col:
                changed = True
            fall_to_col += 1
    return (new,changed)

def merge_horizontal_adjacent_same(mat):
    changed = False
    for i in range(len(mat)):
         for j in range(len(mat)-1):
             if mat[i][j]==mat[i][j+1] and mat[i][j]!=0:
                 mat[i][j] += mat[i][j+1]
                 mat[i][j+1] = 0
                 changed = True
    return (mat,changed)

def reverse(mat):
    new=[]
    for i in range(len(mat)):
        new.append([])
        for j in range(len(mat[0])):
            new[i].append(mat[i][len(mat[0])-j-1])
    return new

def transpose(mat):
    new=[]
    for i in range(len(mat[0])):
        new.append([])
        for j in range(len(mat)):
            new[i].append(mat[j][i])
    return new




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

def game_state(mat, endless_mode = True):
    if not endless_mode:
        for i in range(len(mat)):
            for j in range(len(mat[0])):
                if mat[i][j]==2048:
                    return 'win'
    for i in range(len(mat)-1): #intentionally reduced to check the row on the right and below
        for j in range(len(mat[0])-1): #more elegant to use exceptions but most likely this will be their solution
            if mat[i][j]==mat[i+1][j] or mat[i][j+1]==mat[i][j]:
                return 'not over'
    for i in range(len(mat)): #check for any zero entries
        for j in range(len(mat[0])):
            if mat[i][j]==0:
                return 'not over'
    for k in range(len(mat)-1): #to check the left/right entries on the last row
        if mat[len(mat)-1][k]==mat[len(mat)-1][k+1]:
            return 'not over'
    for j in range(len(mat)-1): #check up/down entries on last column
        if mat[j][len(mat)-1]==mat[j+1][len(mat)-1]:
            return 'not over'
    return 'lose'


if __name__ == '__main__':
    import puzzle
    puzzle.GameGrid()
