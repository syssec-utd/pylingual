def parent(self, type_: Optional[str]=None) -> Optional['WikiText']:
    """Return the parent node of the current object.

        :param type_: the type of the desired parent object.
            Currently the following types are supported: {Template,
            ParserFunction, WikiLink, Comment, Parameter, ExtensionTag}.
            The default is None and means the first parent, of any type above.
        :return: parent WikiText object or None if no parent with the desired
            `type_` is found.
        """
    ancestors = self.ancestors(type_)
    if ancestors:
        return ancestors[0]
    return None