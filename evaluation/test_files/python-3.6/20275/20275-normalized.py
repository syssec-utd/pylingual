def last_two_blanks(src):
    """Determine if the input source ends in two blanks.

    A blank is either a newline or a line consisting of whitespace.

    Parameters
    ----------
    src : string
      A single or multiline string.
    """
    if not src:
        return False
    new_src = '\n'.join(['###\n'] + src.splitlines()[-2:])
    return bool(last_two_blanks_re.match(new_src)) or bool(last_two_blanks_re2.match(new_src))