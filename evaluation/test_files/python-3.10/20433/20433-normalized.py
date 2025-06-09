def define_macro(self, name, themacro):
    """Define a new macro

        Parameters
        ----------
        name : str
            The name of the macro.
        themacro : str or Macro
            The action to do upon invoking the macro.  If a string, a new
            Macro object is created by passing the string to it.
        """
    from IPython.core import macro
    if isinstance(themacro, basestring):
        themacro = macro.Macro(themacro)
    if not isinstance(themacro, macro.Macro):
        raise ValueError('A macro must be a string or a Macro instance.')
    self.user_ns[name] = themacro