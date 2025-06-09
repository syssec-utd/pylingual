def update_prompt(self, name, new_template=None):
    """This is called when a prompt template is updated. It processes
        abbreviations used in the prompt template (like \\#) and calculates how
        many invisible characters (ANSI colour escapes) the resulting prompt
        contains.
        
        It is also called for each prompt on changing the colour scheme. In both
        cases, traitlets should take care of calling this automatically.
        """
    if new_template is not None:
        self.templates[name] = multiple_replace(prompt_abbreviations, new_template)
    invis_chars = _lenlastline(self._render(name, color=True)) - _lenlastline(self._render(name, color=False))
    self.invisible_chars[name] = invis_chars