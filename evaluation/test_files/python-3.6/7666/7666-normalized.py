def from_text(cls, text, lexicon, required=None, first_only=True):
    """
        Generate a Component from a text string, using a Lexicon.

        Args:
            text (str): The text string to parse.
            lexicon (Lexicon): The dictionary to use for the
                categories and lexemes.
            required (str): An attribute that we must have. If a required
                attribute is missing from the component, then None is returned.
            first_only (bool): Whether to only take the first
                match of a lexeme against the text string.

        Returns:
            Component: A Component object, or None if there was no
                must-have field.
        """
    component = lexicon.get_component(text, first_only=first_only)
    if required and required not in component:
        return None
    else:
        return cls(component)