# TODO: serialization and stuff

# all_actions_as_arrow = ['^', 'v', '<', '>']
# all_actions_as_lower = ['u', 'd', 'l', 'r']
# all_actions_as_upper = ['U', 'D', 'L', 'R']


# def action_to_direction(actionCharacter):
#     if actionCharacter in set('^uU'): return dir_up
#     if actionCharacter in set('vdD'): return dir_down
#     if actionCharacter in set('<lL'): return dir_left
#     if actionCharacter in set('>rR'): return dir_right
#     raise Error('Failed to decode action due to invalid actionCharacter: ' + str(actionCharacter))


# for direction, arrow, upper, lower in zip(all_directions, all_actions, all_actions_as_uppercase_letters, all_actions_as_lowercase_letters):
#     assert action_to_direction(arrow) == direction
#     assert action_to_direction(lower) == direction
#     assert action_to_direction(upper) == direction
