def get_component(self, text, required=False, first_only=True):
    """
        Takes a piece of text representing a lithologic description for one
        component, e.g. "Red vf-f sandstone" and turns it into a dictionary
        of attributes.

        TODO:
            Generalize this so that we can use any types of word, as specified
            in the lexicon.
        """
    component = {}
    for (i, (category, words)) in enumerate(self.__dict__.items()):
        if category in SPECIAL:
            continue
        groups = self.find_word_groups(text, category)
        if groups and first_only:
            groups = groups[:1]
        elif groups:
            pass
        else:
            groups = [None]
            if required:
                with warnings.catch_warnings():
                    warnings.simplefilter('always')
                    w = "No lithology in lexicon matching '{0}'"
                    warnings.warn(w.format(text))
        filtered = [self.find_synonym(i) for i in groups]
        if first_only:
            component[category] = filtered[0]
        else:
            component[category] = filtered
    return component