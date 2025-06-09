def set_tex_input_directory(self, tex_input_directory, latex_walker_init_args=None, strict_input=True):
    """
        Set where to look for input files when encountering the ``\\input`` or
        ``\\include`` macro.

        Alternatively, you may also override :py:meth:`read_input_file()` to
        implement a custom file lookup mechanism.

        The argument `tex_input_directory` is the directory relative to which to
        search for input files.

        If `strict_input` is set to `True`, then we always check that the
        referenced file lies within the subtree of `tex_input_directory`,
        prohibiting for instance hacks with '..' in filenames or using symbolic
        links to refer to files out of the directory tree.

        The argument `latex_walker_init_args` allows you to specify the parse
        flags passed to the constructor of
        :py:class:`pylatexenc.latexwalker.LatexWalker` when parsing the input
        file.
        """
    self.tex_input_directory = tex_input_directory
    self.latex_walker_init_args = latex_walker_init_args if latex_walker_init_args else {}
    self.strict_input = strict_input
    if tex_input_directory:
        self.macro_dict['input'] = MacroDef('input', lambda n: self._callback_input(n))
        self.macro_dict['include'] = MacroDef('include', lambda n: self._callback_input(n))
    else:
        self.macro_dict['input'] = MacroDef('input', discard=True)
        self.macro_dict['include'] = MacroDef('include', discard=True)