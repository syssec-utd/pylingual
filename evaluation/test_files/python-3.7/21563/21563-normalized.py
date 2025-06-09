def expand_alias(self, line):
    """ Expand an alias in the command line

        Returns the provided command line, possibly with the first word
        (command) translated according to alias expansion rules.

        [ipython]|16> _ip.expand_aliases("np myfile.txt")
                 <16> 'q:/opt/np/notepad++.exe myfile.txt'
        """
    (pre, _, fn, rest) = split_user_input(line)
    res = pre + self.expand_aliases(fn, rest)
    return res