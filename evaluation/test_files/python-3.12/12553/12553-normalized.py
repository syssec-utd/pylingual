def nest_dictionary(flat_dict, separator):
    """ Nests a given flat dictionary.

    Nested keys are created by splitting given keys around the `separator`.

    """
    nested_dict = {}
    for key, val in flat_dict.items():
        split_key = key.split(separator)
        act_dict = nested_dict
        final_key = split_key.pop()
        for new_key in split_key:
            if not new_key in act_dict:
                act_dict[new_key] = {}
            act_dict = act_dict[new_key]
        act_dict[final_key] = val
    return nested_dict