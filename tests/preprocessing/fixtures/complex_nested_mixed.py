# Complex nested structures with mixed container types
# Tuple of dicts containing tuples and lists
tuple_of_dicts = (
    {1: (2, 3), 'a': [4, 5]},
    {6: [7, 8], 'b': (9, 10)},
)

# Dict of sets containing tuples
dict_of_sets = {
    'x': {(1, 2), (3, 4)},
    'y': {(5, 6), (7, 8)},
}

# List of tuples containing dicts
list_of_tuples = [
    ({'a': 1}, {'b': 2}),
    ({'c': 3}, {'d': 4}),
]

# Tuple of lists containing sets
tuple_of_lists = (
    [{1, 2}, {3, 4}],
    [{5, 6}, {7, 8}],
)

# Nested: dict containing list containing dict containing set
deeply_nested = {
    'level1': [
        {'level2': {1, 2, 3}},
        {'level3': {4, 5, 6}},
    ],
}

# Mixed with empty containers
mixed_empties = {
    'empty_dict': {},
    'empty_list': [],
    'nonempty': [1, 2],
}

print("Done")