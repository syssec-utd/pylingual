def raw_input_ext(prompt='', ps2='... '):
    """Similar to raw_input(), but accepts extended lines if input ends with \\."""
    line = raw_input(prompt)
    while line.endswith('\\'):
        line = line[:-1] + raw_input(ps2)
    return line