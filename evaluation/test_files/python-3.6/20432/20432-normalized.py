def magic(self, arg_s):
    """DEPRECATED. Use run_line_magic() instead.

        Call a magic function by name.

        Input: a string containing the name of the magic function to call and
        any additional arguments to be passed to the magic.

        magic('name -opt foo bar') is equivalent to typing at the ipython
        prompt:

        In[1]: %name -opt foo bar

        To call a magic without arguments, simply use magic('name').

        This provides a proper Python function to call IPython's magics in any
        valid Python code you can type at the interpreter, including loops and
        compound statements.
        """
    (magic_name, _, magic_arg_s) = arg_s.partition(' ')
    magic_name = magic_name.lstrip(prefilter.ESC_MAGIC)
    return self.run_line_magic(magic_name, magic_arg_s)