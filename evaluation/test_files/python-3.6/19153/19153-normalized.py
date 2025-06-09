def _recurse(self, inputs, output, depth, max_depth):
    """We work out all combinations using this internal recursion method"""
    if depth < max_depth:
        for (index, option) in enumerate(inputs):
            my_output = list(output)
            my_output.append(option)
            self._recurse(inputs[index + 1:], my_output, depth + 1, max_depth)
    else:
        self._options.append(output)