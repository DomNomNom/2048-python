from game_logic import new_matrix, merge, find_empty_positions, set_value, dir_up, dir_down, dir_left, dir_right, all_directions

# Provides a mutable interface over game_logic.py
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
        new_mat = merge(self.mat, direction)
        if new_mat == self.mat:  # No change - Don't add stuff to the board.
            return self.mat
        self.mat = new_mat
        self.add_to_random_state(direction)
        self.add_tile()
        return self.mat

    # private

    def add_tile(self):
        # pick an empty tile and put a 2 (sometimes 4) there.
        empties = find_empty_positions(self.mat)
        new_pos = empties[self.rand_mod(len(empties))]
        new_value = 2 if self.rand_mod(10)>0 else 4
        self.mat = set_value(self.mat, new_pos, new_value)
        return self.mat

    random_state_bitwidth = 32  # simulate random_state being kept in a uint32
    random_state_bitmask = 2**random_state_bitwidth - 1
    def add_to_random_state(self, direction):
        assert direction in all_directions
        new_bits = {
            dir_up: 0,
            dir_down: 1,
            dir_left: 2,
            dir_right: 3,
        }[direction]
        self.random_state = ((self.random_state << 2) | new_bits) & self.random_state_bitmask

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

if __name__ == '__main__':
    import puzzle
    puzzle.GameGrid()
