def ancestor(self):
    """This browse node's immediate ancestor in the browse node tree.

        :return:
            The ancestor as an :class:`~.AmazonBrowseNode`, or None.
        """
    ancestors = getattr(self.element, 'Ancestors', None)
    if hasattr(ancestors, 'BrowseNode'):
        return AmazonBrowseNode(ancestors['BrowseNode'])
    return None