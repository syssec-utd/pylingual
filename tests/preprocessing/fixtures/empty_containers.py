# Empty container tests
empty_dict = {}
empty_list = []
empty_tuple = ()
# Note: empty set is set() call, not literal

# Nested empty containers
nested_empty = {
    'a': {},
    'b': [],
    'c': (),
    'd': {'x': {}, 'y': []},
}

print(empty_dict, empty_list, empty_tuple)