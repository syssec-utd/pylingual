# Single element containers with nested types
single_dict_in_list = [{'x': 1}]
single_list_in_dict = {'a': [1]}
single_set_in_tuple = ({1},)
single_tuple_in_set = {(1,)}

# Single element with nested container
single_nested = {'outer': {'inner': [1]}}

print(single_dict_in_list, single_list_in_dict)