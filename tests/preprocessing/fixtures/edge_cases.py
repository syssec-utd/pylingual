# Edge cases
empty_dict = {}
empty_list = []
empty_tuple = ()
# Note: empty set is set() call, not literal
single_in_list = [1]
single_in_tuple = (1,)
single_in_dict = {"x": 1}
nested_empty = {"a": [], "b": {}, "c": ()}
deep_nesting = [[[{"x": {1, (2, 3)}}]]]
print(empty_dict, empty_list, empty_tuple, single_in_list, single_in_tuple, single_in_dict, nested_empty, deep_nesting)
