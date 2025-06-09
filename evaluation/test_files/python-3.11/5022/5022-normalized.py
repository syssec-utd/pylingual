def __get_old_filepath(self, f):
    """Get the old filepath of a moved/renamed file.

        Moved or renamed files can be found in the log with any of the
        next patterns:
          'old_name => new_name'
          '{old_prefix => new_prefix}/name'
          'name/{old_suffix => new_suffix}'

        This method returns the filepath before the file was moved or
        renamed.
        """
    i = f.find('{')
    j = f.find('}')
    if i > -1 and j > -1:
        prefix = f[0:i]
        inner = f[i + 1:f.find(' => ', i)]
        suffix = f[j + 1:]
        return prefix + inner + suffix
    elif ' => ' in f:
        return f.split(' => ')[0]
    else:
        return f